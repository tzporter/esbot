# End-to-End (E2E) Testing Setup

This document describes the setup, configuration, and execution instructions for the Automated E2E test suite of the ESBot application.

## Framework Choice

We have chosen **Cypress** for our E2E testing framework. Cypress provides an interactive visual test runner, excellent debugging capabilities, and built-in auto-waiting mechanisms which eliminate the need for brittle `sleep()` statements. It is perfectly suited for testing our single-page application.

## Prerequisites

- **Node.js** (v18 or higher) installed on your machine.
- The ESBot application running locally (Backend + Frontend). As per our current setup, the application is containerized and accessible at `http://localhost:8501`.

## Installation Steps

1. Navigate to the root of the project (or your frontend directory) in your terminal.
2. Initialize a Node project (if `package.json` does not exist):
   npm init -y
3. Install Cypress as a development dependency:
   npm install cypress --save-dev

## Starting the Application

Before running the tests, ensure the application is up and running using Docker with the mock LLM enabled:

1. Ensure your `.env` file is configured properly (based on `.env.example`) with `LLM_PROVIDER=mock`.
2. Start the application:
   docker compose up --build

   The frontend should now be available at `http://localhost:8501`.

## Running the Tests

You can run the Cypress tests in two modes:

- **Interactive / Headed Mode (for debugging and visualization):**
  npx cypress open
  _(Then select "E2E Testing" and choose your browser)._

- **Headless Mode (for CI/CD pipelines):**
  npx cypress run
