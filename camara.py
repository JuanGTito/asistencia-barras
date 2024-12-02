import cv2
from pyzbar.pyzbar import decode

def scan_code():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        return None

    detected_codes = set()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error al leer el fotograma de la cámara.")
            continue

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')

            if barcode_data not in detected_codes:
                detected_codes.add(barcode_data)
                print(f'Dato del código de barras: {barcode_data}')


                cap.release()
                cv2.destroyAllWindows()

                return barcode_data

        cv2.imshow("Código de Barras Scanner", frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
