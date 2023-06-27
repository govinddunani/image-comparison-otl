# image-comparison-otl

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




