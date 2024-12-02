import cv2
from pyzbar.pyzbar import decode

def scan_code():
    cap = cv2.VideoCapture(2)  # Cambia el índice según sea necesario

    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        return None

    detected_codes = set()  # Conjunto para almacenar códigos únicos detectados

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error al leer el fotograma de la cámara.")
            continue

        # Decodificar códigos de barras en el fotograma
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            barcode_data = obj.data.decode('utf-8')

            # Verificar si el código ya fue detectado
            if barcode_data not in detected_codes:
                detected_codes.add(barcode_data)  # Agregar a la lista de detectados
                print(f'Dato del código de barras: {barcode_data}')

                # Cerrar la cámara y las ventanas después de detectar un código
                cap.release()
                cv2.destroyAllWindows()

                # Retorna el dato del código de barras y cierra el módulo scan_code
                return barcode_data

        # Mostrar el fotograma en una ventana
        cv2.imshow("Código de Barras Scanner", frame)

        # Salir manualmente con la tecla 'q' (opcional, para poder terminar el escaneo)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Asegurarse de cerrar la cámara y las ventanas si no se detecta ningún código
    cap.release()
    cv2.destroyAllWindows()
    return None
