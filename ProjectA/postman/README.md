# Postman API checks

1. In a terminal, open `ProjectA` and run `npm start`.
2. In Postman, select **Import** and import both JSON files in this folder.
3. Select the **Bond Sports - Local** environment.
4. Open **Bond Sports API** and use **Run collection** to execute all checks, or send one request at a time.

The collection covers successful login, invalid credentials, a missing password, and malformed JSON. Each request contains automated assertions under the **Tests** tab.
