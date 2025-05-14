import cv2
import numpy as np
import sys

def initialize_video_capture(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("動画ファイルを開けませんでした。ファイル名を確認してください。")
        exit()
    ret, frame1 = cap.read()  
    return cap, cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

def calculate_optical_flow(prvs, next, roi):
    x, y, w, h = roi
    roi_prvs = prvs[y:y+h, x:x+w]
    roi_next = next[y:y+h, x:x+w]
    flow = cv2.calcOpticalFlowFarneback(roi_prvs, roi_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    dx = flow[..., 0]
    dy = flow[..., 1]
    mag = np.sqrt(dx**2 + dy**2)
    return flow, mag

def draw_arrows(frame, flow, roi, mag, color=(0, 255, 0), scale=10, arrow_length=5, min_magnitude=1):
    x, y, w, h = roi
    for y_pos in range(0, h, scale):
        for x_pos in range(0, w, scale):
            if mag[y_pos, x_pos] > min_magnitude:
                dx, dy = flow[y_pos, x_pos]
                length = min(mag[y_pos, x_pos], arrow_length)
                end_x = int(x + x_pos + length * dx)
                end_y = int(y + y_pos + length * dy)
                thickness = 2
                cv2.arrowedLine(frame, (x + x_pos, y + y_pos), (end_x, end_y), color, thickness, tipLength=0.05)

video_path = input("動画ファイルの名前を入力してください (例: video.mp4): ")
try:
    pixel_to_distance = float(input("1ピクセルあたりの距離 (mm) を入力してください: "))
    if pixel_to_distance <= 0:
        raise ValueError("1ピクセルあたりの距離は正の値である必要があります。")
except ValueError as e:
    print(f"入力エラー: {e}")
    exit()

cap, prvs = initialize_video_capture(video_path)
ret, frame = cap.read()
if not ret:
    print("動画の読み込みに失敗しました。")
    exit()

# ROIをコード内で任意の座標に変更する際には、以下のコードを切り替えて下さい。
roi = cv2.selectROI("ROI選択", frame, fromCenter=False, showCrosshair=True)
# 上記コードをコメントアウトし、下のコメントアウトを外してください。（x軸座標, y軸座標, 幅, 高さ）
# roi = (300, 300, 50, 50)

cv2.destroyAllWindows()

frame_count = 1
total_95th_percentile_movement = 0.0  

while True: 
    ret, frame2 = cap.read()
    if not ret:
        break

    next_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    next_gray = cv2.blur(next_gray, (5, 5))  

    flow, mag_full = calculate_optical_flow(prvs, next_gray, roi)

    valid_magnitudes = mag_full[mag_full > 1]
    if valid_magnitudes.size > 0:
        percentile_95_movement = np.percentile(valid_magnitudes, 95)  
        percentile_95_movement_px = percentile_95_movement
        percentile_95_movement_distance = percentile_95_movement_px * pixel_to_distance
        total_95th_percentile_movement += percentile_95_movement_distance  
        print(f"{frame_count}フレーム目の動き: {percentile_95_movement_distance:.2f} mm")  
    else:
        print(f"{frame_count}フレーム目の動き: 検出されませんでした。")
        
    draw_arrows(frame2, flow, roi, mag_full, (0, 255, 0))
    frame2_with_roi = frame2.copy()
    cv2.rectangle(frame2_with_roi, roi[:2], (roi[0] + roi[2], roi[1] + roi[3]), (255, 0, 0), 2)
    cv2.imshow('frame2', frame2_with_roi)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    prvs = next_gray
    frame_count += 1

print("\n-------------------------------------\n")
print(f"移動距離の合計の推定値: {total_95th_percentile_movement:.2f} mm")  
print("\n-------------------------------------\n")
print(f"選択したROIの大きさ: 幅={roi[2]}, 高さ={roi[3]}")
print("\n-------------------------------------\n")
print(f"Pythonのバージョン: {sys.version}")
print(f"OpenCVのバージョン: {cv2.__version__}")
print(f"NumPyのバージョン: {np.__version__}")

cap.release()
cv2.destroyAllWindows()
