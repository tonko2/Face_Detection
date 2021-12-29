import time
import cv2
import win32gui
import ctypes

def foreground(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd,1)
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        return False


cap = cv2.VideoCapture(0)

before = None
while True:
    #  OpenCVでWebカメラの画像を取り込む
    ret, frame = cap.read()

    frame = cv2.resize(frame, (int(frame.shape[1]), int(frame.shape[0])))

    # 取り込んだフレームに対して差分をとって動いているところが明るい画像を作る
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if before is None:
        before = gray.copy().astype('float')
        continue

    # 現フレームと前フレームの加重平均を使うと良いらしい
    cv2.accumulateWeighted(gray, before, 0.5)
    mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(before))

    # 動いているエリアの面積を計算してちょうどいい検出結果を抽出する
    thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)[1]
    # 輪郭データに変換しくれるfindContours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    for cnt in contours:
        #輪郭の面積を求めてくれるcontourArea
        area = cv2.contourArea(cnt)
        if max_area < area and area < 10000 and area > 2000:
            max_area = area

    # 動いているエリアがそこそこ大きければ、動いてるのを検出して、titleのウィンドウをアクティブ化
    if max_area > 2000:
        title = 'Discord'
        try:
            win32gui.EnumWindows(foreground, title)
        except Exception as e:
            time.sleep(1)
            pass

    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()