Authorize credentials for a desktop application
To authenticate end users and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers. If your app runs on multiple platforms, you must create a separate client ID for each platform.

    In the Google Cloud console, go to Menu menu > Google Auth platform > Clients.

    Go to Clients
    Click Create Client.
    Click Application type > Desktop app.
    In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
    Click Create.

    The newly created credential appears under "OAuth 2.0 Client IDs."
    Save the downloaded JSON file as credentials.json, and move the file to your working directory.
