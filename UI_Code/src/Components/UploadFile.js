import React, { useState } from "react";
import img from "./img.png";
import Jump from "react-reveal/Jump";
import NavBar from "./NavBar";
import { uploadFile } from 'react-s3';
import { MDBBtn } from 'mdbreact';

const S3_BUCKET ='cputablefiles';
const REGION ='US East (N. Virginia) us-east-1';
const ACCESS_KEY ='uspNNZFzzeyk4DtAWV67zCuzDPzKDfLo8MiXJ34+';
const SECRET_ACCESS_KEY ='oaHIUb72MODSkx+QtXhyJWZLT6rW6XL0nYF+wT7w';

const config = {
    bucketName: S3_BUCKET,
    region: REGION,
    accessKeyId: ACCESS_KEY,
    secretAccessKey: SECRET_ACCESS_KEY,
}

function UploadFile()  {
    // const fileInput = useRef();

    // const handleClick = (event) => {
    //     event.preventDefault();
    //     let file = fileInput.current.files[0];
    //     console.log(file);
    //     const config = {
    //         bucketName: process.env.REACT_APP_BUCKET_NAME,
    //         dirName: process.env.REACT_APP_DIR_NAME,
    //         region: process.env.REACT_APP_REGION,
    //         accessKeyId: process.env.REACT_APP_ACCESS_ID,
    //         secretAccessKey: process.env.REACT_APP_ACCESS_KEY,
    //     };
    //     const ReactS3Client = new S3(config);
    //     console.log("here");
    //     ReactS3Client.uploadFile(file).then((data) => {
    //         console.log(data);
    //         if (data.status === 204) {
    //         console.log("success");
    //         } else {
    //         console.log("fail");
    //         }
    //     });
    //     console.log("Uploaded");
    //   };

      const [selectedFile, setSelectedFile] = useState(null);

      const handleFileInput = (e) => {
          setSelectedFile(e.target.files[0]);
      }
  
      const handleUpload = async (file) => {
          uploadFile(file, config)
              .then(data => console.log(data))
              .catch(err => console.error(err))
      }
        return (
            <div>
                <NavBar/>
                <header className="jumbotron text-center"
                style={{
                    backgroundImage: `url(${img})`,
                    paddingTop: "150px",
                    backgroundPosition: "center",
                    backgroundRepeat: "no - repeat",
                    backgroundSize: "cover",
                    width: "100%",
                    }}></header>
                
                <div >
                    <Jump>
                        <h1 className="row justify-content-center" style={{ display: "center", fontFamily: "Lucida Console" }}>
                            Insurance
                        </h1>
                    </Jump>
                    {/* <input type="file" onChange={handleFileInput} />
                    
                    <button onClick={() => handleUpload(selectedFile)}> Upload to S3</button> */}
                    <span >
                        <h3 className="row justify-content-center">Claim your insurance now</h3>
                        <div className="row justify-content-center">
                        <input
                            type="file"
                            onChange={handleFileInput}
                            // ref={fileInput}                          
                        />
                        <MDBBtn
                            gradient="aqua"
                            // onClick={handleClick}
                            onClick={() => handleUpload(selectedFile)}
                        >
                                Submit
                        </MDBBtn> 
                        </div>
                     </span>
                </div>
            </div>
        )
    }

export default UploadFile;