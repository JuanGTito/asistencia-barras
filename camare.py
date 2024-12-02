import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    decoded_objets = decode(frame)

    for obj in decoded_objets:
        barcode_data = obj.data.decode('utf-8')
        barcode_type = obj.type

        print(f'Tipo de codigo de barras: {barcode_data}')
        print(f'Dato del codigo de barras: {barcode_type}')

    cv2.imshow("Codigo de Barras Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()