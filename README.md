# image-comparison-otl
Sure! Here's a step-by-step guide on how to install Visual Studio Code (VS Code) and set up a Python development environment with the necessary software:

Step 1: Download and Install Visual Studio Code

1. Visit the official Visual Studio Code website at https://code.visualstudio.com/.
2. Click on the "Download" button to download the installer for your operating system (Windows, macOS, or Linux).
3. Run the installer and follow the on-screen instructions to complete the installation of Visual Studio Code.

Step 2: Install Python Extension in VS Code

1. Launch Visual Studio Code after the installation is complete.
2. In the left sidebar, click on the Extensions icon (four squares icon), or use the shortcut `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS).
3. In the Extensions search bar, type "Python" and press Enter.
4. Look for the official "Python" extension by Microsoft and click on the "Install" button.
5. After installation, you may need to reload or restart Visual Studio Code.

Step 3: Create a New Python Project

1. Open Visual Studio Code.
2. Click on the "Explorer" icon in the left sidebar (folder icon) or use the shortcut `Ctrl+Shift+E` (Windows/Linux) or `Cmd+Shift+E` (macOS).
3. Click on the "Open Folder" button and select a directory where you want to create your Python project.
4. Once the folder is open in Visual Studio Code, click on the "New File" button in the Explorer sidebar and save the file with a `.py` extension (e.g., `main.py`).

Step 4: Set Up Python Environment

1. Open the integrated terminal in Visual Studio Code by clicking on the "Terminal" menu at the top and selecting "New Terminal." Alternatively, use the shortcut `Ctrl+` (backtick) (Windows/Linux) or `Ctrl+`` (backtick) (macOS).
2. In the terminal, type the following command to create a virtual environment:
   ```
   python3 -m venv myenv
   ```
   Replace `myenv` with the desired name for your virtual environment.
3. Activate the virtual environment by running the appropriate command based on your operating system:
   - Windows:
     ```
     myenv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source myenv/bin/activate
     ```
4. Your terminal prompt should now indicate that you are inside the virtual environment.
5. Install required Python packages using `pip`. For example:
   ```
   pip install flask flask-cors pillow
   ```

You have now set up Visual Studio Code with the Python extension and created a Python project with the necessary software installed. You can start writing your Python code in the `.py` file you created and execute it using the integrated terminal within Visual Studio Code. 
Cloning the repository is a good approach to get the backend and frontend code on your local machine. Here are the steps you can follow:

1. Open your terminal or command prompt and navigate to the desired directory where you want to clone the repository.

2. Clone the repository using the command:
   ```
   git clone <repository_url>
   ```

3. Once the cloning process is complete, navigate to the backend folder in the cloned repository:
   ```
   cd <repository_folder>/backend
   ```

4. Create a virtual environment using VS Code's integrated terminal:
   ```
   virtualenv image_comparison
   ```

5. Activate the virtual environment:
   ```
   image_comparison\Scripts\activate
   ```

6. Install the required Python dependencies from the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```

7. Run the backend server using the following command:
   ```
   python compare_v3.py
   ```

   This will start the backend server, and it will be accessible at `localhost:5000`.
run the frontend and backend server seperately and do not close the backend server while running the frontend server.

Now, it's time to set up the frontend:

1. Open a new terminal or command prompt window.

2. Navigate to the frontend folder in the cloned repository:
   ```
   cd <repository_folder>/frontend
   ```

3. Install the required dependencies for the frontend:
   ```
   npm install
   ```

4. Start the frontend development server:
   ```
   npm start
   ```

   The frontend server will start, and you can access it at `localhost:3000`.

You have now successfully set up and run both the backend and frontend servers. The backend is accessible at `localhost:5000`, and the frontend is accessible at `localhost:3000`.




