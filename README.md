## Project to demonstrate simple TCP socket communication in python

### Instructions to run the project:
1. Clone the repository
2. `cd` into the project directory
3. Change settings in `settings.env`
4. Create a virtual environment using `python3 -m venv venv`
5. Activate the virtual environment using `source venv/bin/activate`
6. Install the dependencies using `pip install -r requirements.txt`
7. RSA is used for encryption. Generate two pairs of keys using `python -m app.generate_keys client` and `python -m app.generate_keys server`. This will generate `client_public.pem`, `client_private.pem`, `server_public.pem`, `server_private.pem` files. These files are already present in the repository.
8. Start server using `python -m app.main server_private.pem client_public.pem`. Keep the server running.
9. Start client using `python -m app.client  server_public.pem client_private.pem`. It takes you to shell session where you can send requests to the server.
10. Run tests using `python -m pytest -v -s`