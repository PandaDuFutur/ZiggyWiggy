import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import cgi

# Dossier pour stocker les fichiers reçus
data_folder = "server_files"
os.makedirs(data_folder, exist_ok=True)

class FileServerHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        """Gérer l'upload de fichiers."""
        if self.path == '/upload':
            # Parse les données multipart/form-data
            content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
            if content_type != 'multipart/form-data':
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Type de contenu non support\u00e9")
                return
            
            pdict['boundary'] = pdict['boundary'].encode()
            pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
            fields = cgi.parse_multipart(self.rfile, pdict)

            if 'file' in fields:
                uploaded_file = fields['file'][0]
                filename = fields['file'][1].decode('utf-8')  # Nom du fichier envoyé
                filepath = os.path.join(data_folder, filename)

                with open(filepath, "wb") as f:
                    f.write(uploaded_file)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Fichier {filename} enregistr\u00e9 avec succ\u00e8s.".encode())
                return
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Aucun fichier fourni")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint non trouv\u00e9")
    
    def do_GET(self):
        """Gérer les requêtes GET pour la liste et le téléchargement de fichiers."""
        url = urlparse(self.path)
        if url.path == '/files':
            # Liste des fichiers disponibles
            files = os.listdir(data_folder)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("\n".join(files).encode())
        elif url.path.startswith('/files/'):
            # Téléchargement d'un fichier spécifique
            filename = os.path.basename(url.path)
            filepath = os.path.join(data_folder, filename)

            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header("Content-Disposition", f"attachment; filename={filename}")
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", os.path.getsize(filepath))
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Fichier non trouv\u00e9")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint non trouv\u00e9")

if __name__ == "__main__":
    # Configuration du serveur
    server_address = ('', 5000)  # Écoute sur toutes les interfaces, port 5000
    httpd = HTTPServer(server_address, FileServerHandler)
    print("Serveur démarré sur le port 5000...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Arrêt du serveur.")
        httpd.server_close()
