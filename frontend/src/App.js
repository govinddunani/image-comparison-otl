import React, { useState } from 'react';
import JSZip from 'jszip';
import './App.css'; // Import the CSS file for styling


function App() {
  const [image1, setImage1] = useState(null);
  const [image2, setImage2] = useState(null);
  const [comparedImageRed, setComparedImageRed] = useState(null);
  const [comparedImageGreen, setComparedImageGreen] = useState(null);
  const [zip_path_red, setZipPathRed] = useState(null);
  const [zip_filename_red, setZipFilenameRed] = useState(null);
  const [zip_path_green, setZipPathGreen] = useState(null);
  const [zip_filename_green, setZipFilenameGreen] = useState(null);
  const [column, setColumn] = useState(null);
  const [row, setRow] = useState(null);
  const [subImages, setSubImages] = useState([]);
  const [loading, setLoading] = useState(false);


  const handleImage1Change = (event) => {
    setImage1(event.target.files[0]);
  };


  const handleImage2Change = (event) => {
    setImage2(event.target.files[0]);
  };


  const handleCompare = async () => {
    setLoading(true);
    if (!image1 || !image2) {
      alert('Please select two images.');
      return;
    }


    const formData = new FormData();
    formData.append('image1', image1);
    formData.append('image2', image2);


    const response = await fetch('http://localhost:5000/compare', {
      method: 'POST',
      body: formData
    });


    if (response.ok) {
      const data = await response.json();
      setComparedImageRed(data.compared_image_red);
      setComparedImageGreen(data.compared_image_green);
      setZipPathRed(data.zip_path_red);
      setZipFilenameRed(data.zip_filename_red);
      setZipPathGreen(data.zip_path_green);
      setZipFilenameGreen(data.zip_filename_green);
      setColumn(data.column);
      setRow(data.row);
    }
    
    setLoading(false);
  };


  const handleDisplaySubImagesRed = async (zip_path, zip_filename) => {
    console.log(zip_path_red);
    const response = await fetch(
      `http://localhost:5000/download_zip?zip_path=${encodeURIComponent(
        zip_path
      )}&zip_filename=${encodeURIComponent(zip_filename)}`
    );


    if (response.ok) {
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const newWindow = window.open(url);

      const document = newWindow.document.open();
      document.write('<html><head><title>Sub-Images</title></head><body></body></html>');
      document.close();

      const zip = new JSZip();
      const zipContents = await zip.loadAsync(blob);

      const sortedFiles = Object.entries(zipContents.files)
        .filter(([relativePath, file]) => file.dir === false)
        .sort(([relativePathA, fileA], [relativePathB, fileB]) => {
          const indexA = parseInt(relativePathA.split('_').pop(), 10);
          const indexB = parseInt(relativePathB.split('_').pop(), 10);
          return indexA - indexB;
        });

      const containerElement = newWindow.document.createElement('div');
      containerElement.className = 'image-grid'; // Apply custom CSS class for styling
      newWindow.document.body.appendChild(containerElement);

      const numColumns = column+1; // Define the number of columns
      const loadPromises = sortedFiles.map(async ([relativePath, file]) => {
        const subImageBlob = await file.async('blob');
        const subImageURL = URL.createObjectURL(subImageBlob);

        // Create an image element and append it to the body of the new window
        const imageElement = newWindow.document.createElement('img');
        imageElement.src = subImageURL;
        newWindow.document.body.appendChild(imageElement);

        // Add a space between images
        const spaceElement = newWindow.document.createTextNode(' ');
        newWindow.document.body.appendChild(spaceElement);

        // Check if the number of images added is divisible by the number of columns
        if (newWindow.document.body.childElementCount % numColumns === 0) {
          // Insert a line break after the specified number of columns
          const lineBreakElement = newWindow.document.createElement('br');
          newWindow.document.body.appendChild(lineBreakElement);
        }
      });


      await Promise.all(loadPromises);
    }
  };


  const getBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result.split(',')[1]);
      reader.onerror = (error) => reject(error);
    });
  };


  return (
    <div className="app-container">
      <h1 className="app-title">Welcome to the Image Comparison App</h1>
      <div className="upload-section">
        <h2>Upload Images:</h2>
        <input type="file" onChange={handleImage1Change} className="image-upload" />
        <input type="file" onChange={handleImage2Change} className="image-upload" />
        <button onClick={handleCompare} className="compare-button">Compare Images</button>
      </div>
      {loading && <div className="loader">Loading...</div>}

      <div class="image-container">
      {comparedImageRed && (
        <div className="compared-image-section">
          <h2>Compared Image (Red):</h2>
          <img src={`data:image/png;base64,${comparedImageRed}`} alt="Compared Image (Red)" className="compared-image" />
          <button onClick={() => handleDisplaySubImagesRed(zip_path_red, zip_filename_red)} className="view-button">View Red Sub-Images</button>
        </div>
      )}
      {comparedImageGreen && (
        <div className="compared-image-section">
          <h2>Compared Image (Green):</h2>
          <img src={`data:image/png;base64,${comparedImageGreen}`} alt="Compared Image (Green)" className="compared-image" />
          <button onClick={() => handleDisplaySubImagesRed(zip_path_green, zip_filename_green)} className="view-button">View Green Sub-Images</button>
        </div>
      )}
    </div>
    </div>
  );
}


export default App;
