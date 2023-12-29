<h1 align="center">Soca</h1>

Soca is a system that wraps a CCTV NVR and expose it as API. This app built with [FastAPI](https://fastapi.tiangolo.com//).

## Getting Started

You can start editing the app by modifying files inside the `soca` folder. The app auto-updates as you edit the file.

## Project Structure

```
.
└── soca
    ├── application     # Application business rules
    ├── domain          # Enterprise business rules
    ├── infrastructure  # Framework and drivers
    └── presentation    # User interface
```

## Development

1. Set up the development environment

   You need to set up your development environment before you can do anything.

   Install [Python](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/#installation).

2. Install the dependencies

   ```bash
   poetry install
   ```

3. Run in development mode

   ```bash
   uvicorn soca.main:app --host 0.0.0.0 --reload
   ```

   Open [http://localhost:8000](http://localhost:3000) with your browser to see the result. You can also check the API documentation at [http://localhost:8000/docs](http://localhost:3000/docs).

## Deployment

1. Start the Uvicorn server

   ```bash
   uvicorn soca.main:app --host 0.0.0.0 --port 80
   ```

## Learn More

To learn more about FastAPI, take a look at the following resources:

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - learn about Next.js features and API.
