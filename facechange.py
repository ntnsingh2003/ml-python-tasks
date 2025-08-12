"""
face_swap_live.py
Real-time face swap between two faces in webcam feed using MediaPipe + OpenCV.

Run:
    python face_swap_live.py
"""

import cv2
import numpy as np
import mediapipe as mp
import time

mp_face_mesh = mp.solutions.face_mesh

# Configuration
MAX_NUM_FACES = 4  # detect up to 4 faces (we'll swap the two largest)
DRAW_LANDMARKS = False

# Choose which landmark indices to use for face region:
# We'll take a set of points covering the whole face (jaw, eyes, nose, mouth, cheeks)
# Using many points helps alignment and warp quality. MediaPipe has 468 landmarks.
# We'll use a commonly used subset that roughly covers the outer face & interior.
FACE_POINT_INDICES = list(range(0, 468))  # use all landmarks (slower but robust)

# Utilities ---------------------------------------------------------------
def landmarks_to_np(landmarks, w, h, indices=None):
    """Convert normalized landmarks to Nx2 array of pixel coords."""
    if indices is None:
        indices = range(len(landmarks))
    pts = []
    for i in indices:
        lm = landmarks[i]
        x, y = int(lm.x * w), int(lm.y * h)
        pts.append((x, y))
    return np.array(pts, dtype=np.int32)

def rect_from_points(points):
    x, y, w, h = cv2.boundingRect(points)
    return (x, y, x + w, y + h)

def apply_affine_transform(src, src_tri, dst_tri, size):
    # Compute affine transform and apply it to src patch
    warp_mat = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))
    dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return dst

def warp_triangle(img1, img2, t1, t2):
    # Warp triangular region t1 from img1 to img2 into t2
    # t1, t2: lists/arrays of 3 points
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    t1_rect = []
    t2_rect = []
    t2_rect_int = []

    for i in range(3):
        t1_rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2_rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2_rect_int.append((int(t2[i][0] - r2[0]), int(t2[i][1] - r2[1])))

    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2_rect_int), (1.0, 1.0, 1.0), 16, 0)

    img1_rect = img1[r1[1]:r1[1]+r1[3], r1[0]:r1[0]+r1[2]]
    size = (r2[2], r2[3])
    img2_rect = apply_affine_transform(img1_rect, t1_rect, t2_rect, size)

    img2_subsection = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]]
    # Blend
    img2_subsection = img2_subsection * (1 - mask) + img2_rect * mask
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2_subsection

# Triangulation helper ---------------------------------------------------
def calculate_delaunay_triangles(rect, points):
    # rect is bounding rectangle (x, y, x+w, y+h)
    subdiv = cv2.Subdiv2D((rect[0], rect[1], rect[2], rect[3]))
    for p in points:
        subdiv.insert((int(p[0]), int(p[1])))
    triangle_list = subdiv.getTriangleList()
    delaunay_tri = []
    pts = np.array(points)
    for t in triangle_list:
        pts_tri = [(t[0], t[1]), (t[2], t[3]), (t[4], t[5])]
        idx = []
        for p in pts_tri:
            # find index of point p
            # Because of float rounding, find the nearest point
            distances = np.linalg.norm(pts - p, axis=1)
            min_idx = np.argmin(distances)
            if distances[min_idx] < 20:  # threshold tolerance
                idx.append(int(min_idx))
        if len(idx) == 3:
            delaunay_tri.append(tuple(idx))
    # Remove duplicates
    delaunay_tri = list(dict.fromkeys(delaunay_tri))
    return delaunay_tri

# Main face-swap logic ---------------------------------------------------
def swap_faces_between(img, pts1, pts2, tri_indices):
    """Warp face from pts1 onto pts2 region in img and return swapped face image (same size)."""
    img2 = img.copy().astype(np.float32)
    warped_face = np.zeros_like(img2, dtype=np.float32)

    # Warp triangles from source (pts1) to destination (pts2)
    for tri in tri_indices:
        t1 = [tuple(pts1[tri[i]]) for i in range(3)]
        t2 = [tuple(pts2[tri[i]]) for i in range(3)]
        warp_triangle(img, warped_face, t1, t2)

    # Create mask for destination convex hull
    hull2 = cv2.convexHull(np.array(pts2), returnPoints=True)
    mask = np.zeros(img.shape, dtype=img.dtype)
    cv2.fillConvexPoly(mask, np.int32(hull2), (255, 255, 255))
    center = (int((rect[0] + rect[2]) / 2), int((rect[1] + rect[3]) / 2))  # placeholder (updated later)

    # We'll compute center for seamlessClone using bounding rect of hull2
    r = cv2.boundingRect(hull2)
    center = (int(r[0] + r[2]/2), int(r[1] + r[3]/2))

    output = cv2.seamlessClone(np.uint8(warped_face), img, mask, center, cv2.NORMAL_CLONE)
    return output

# Improved swap function that returns two swapped frames (A->B and B->A)
def swap_pair(img, ptsA, ptsB):
    h, w = img.shape[:2]

    # bounding rects
    rectA = cv2.boundingRect(np.array(ptsA))
    rectB = cv2.boundingRect(np.array(ptsB))

    # Use points normalized to local bounding box for Delaunay to be stable
    # But to keep correspondence, we compute Delaunay on one set (ptsA) in full image coords
    tri_indices = calculate_delaunay_triangles((0, 0, w, h), ptsA.tolist())

    # Warp A->B
    warped_A_on_B = img.copy().astype(np.float32) * 0  # empty
    for tri in tri_indices:
        tA = [tuple(ptsA[tri[i]]) for i in range(3)]
        tB = [tuple(ptsB[tri[i]]) for i in range(3)]
        warp_triangle(img, warped_A_on_B, tA, tB)

    hullB = cv2.convexHull(np.array(ptsB), returnPoints=True)
    maskB = np.zeros(img.shape, dtype=img.dtype)
    cv2.fillConvexPoly(maskB, np.int32(hullB), (255, 255, 255))
    rB = cv2.boundingRect(hullB)
    centerB = (int(rB[0] + rB[2]/2), int(rB[1] + rB[3]/2))
    output_AonB = cv2.seamlessClone(np.uint8(warped_A_on_B), img, maskB, centerB, cv2.NORMAL_CLONE)

    # Warp B->A
    warped_B_on_A = img.copy().astype(np.float32) * 0
    for tri in tri_indices:
        tA = [tuple(ptsA[tri[i]]) for i in range(3)]
        tB = [tuple(ptsB[tri[i]]) for i in range(3)]
        # warp from img area of B to warped_B_on_A at location of A by swapping arguments
        warp_triangle(img, warped_B_on_A, tB, tA)

    hullA = cv2.convexHull(np.array(ptsA), returnPoints=True)
    maskA = np.zeros(img.shape, dtype=img.dtype)
    cv2.fillConvexPoly(maskA, np.int32(hullA), (255, 255, 255))
    rA = cv2.boundingRect(hullA)
    centerA = (int(rA[0] + rA[2]/2), int(rA[1] + rA[3]/2))
    output_BonA = cv2.seamlessClone(np.uint8(warped_B_on_A), img, maskA, centerA, cv2.NORMAL_CLONE)

    # Combine outputs smartly: overlay swapped area only
    # We'll construct final frame where face A area is replaced with B->A result,
    # and face B area is replaced with A->B result.
    final = img.copy()
    # face A region replace
    maskA_gray = cv2.cvtColor(maskA, cv2.COLOR_BGR2GRAY)
    _, mA_bin = cv2.threshold(maskA_gray, 1, 255, cv2.THRESH_BINARY)
    mA_inv = cv2.bitwise_not(mA_bin)
    final = cv2.bitwise_and(final, final, mask=mA_inv)
    faceA_region = cv2.bitwise_and(output_BonA, output_BonA, mask=mA_bin)
    final = cv2.add(final, faceA_region)

    # face B region replace
    maskB_gray = cv2.cvtColor(maskB, cv2.COLOR_BGR2GRAY)
    _, mB_bin = cv2.threshold(maskB_gray, 1, 255, cv2.THRESH_BINARY)
    mB_inv = cv2.bitwise_not(mB_bin)
    final = cv2.bitwise_and(final, final, mask=mB_inv)
    faceB_region = cv2.bitwise_and(output_AonB, output_AonB, mask=mB_bin)
    final = cv2.add(final, faceB_region)

    return final

# Main loop ---------------------------------------------------------------
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        exit()

    # Setup MediaPipe Face Mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                      max_num_faces=MAX_NUM_FACES,
                                      refine_landmarks=True,
                                      min_detection_confidence=0.5,
                                      min_tracking_confidence=0.5)

    prev_time = 0
    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(img_rgb)

        h, w = frame.shape[:2]
        faces = []
        # gather faces and their areas to choose two largest
        if results.multi_face_landmarks:
            for fidx, face_landmarks in enumerate(results.multi_face_landmarks):
                pts = landmarks_to_np(face_landmarks.landmark, w, h, indices=FACE_POINT_INDICES)
                # bounding area size as proxy
                x, y, x2, y2 = rect_from_points(pts)
                area = (x2 - x) * (y2 - y)
                faces.append({
                    "idx": fidx,
                    "landmarks": pts,
                    "area": area,
                    "bbox": (x, y, x2, y2),
                })

        if len(faces) >= 2:
            # sort faces by area and take top two
            faces = sorted(faces, key=lambda x: x["area"], reverse=True)
            faceA = faces[0]
            faceB = faces[1]

            ptsA = faceA["landmarks"]
            ptsB = faceB["landmarks"]

            # try swapping
            try:
                output = swap_pair(frame, ptsA, ptsB)
            except Exception as e:
                # fallback: show original if something goes wrong
                print("Swap error:", e)
                output = frame.copy()
        else:
            output = frame.copy()

        # FPS display
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0.0
        prev_time = curr_time
        cv2.putText(output, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        # Optional: draw landmarks for debugging
        if DRAW_LANDMARKS and results.multi_face_landmarks:
            for lm in results.multi_face_landmarks:
                for pt in lm.landmark:
                    x, y = int(pt.x * w), int(pt.y * h)
                    cv2.circle(output, (x,y), 1, (0,255,0), -1)

        cv2.imshow("Live Face Swap (press q to quit)", output)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
