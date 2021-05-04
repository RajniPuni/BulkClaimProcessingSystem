import React, { useState } from 'react';
import Icon1 from '../../../images/doubt.svg';
import Icon2 from '../../../images/access.svg';
import Icon3 from '../../../images/Premium.svg'
import { ServicesContainer, ServicesH1, ServicesH2, ServicesCard, ServicesIcon, ServicesP, ServicesWrapper } from './ServiceElements';
import { uploadFile } from 'react-s3';
import { MDBBtn } from 'mdbreact';
import Swal from "sweetalert2";

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
const Service = () => {
    const [selectedFile, setSelectedFile] = useState(null);

      const handleFileInput = (e) => {
          setSelectedFile(e.target.files[0]);
      }
  
    const handleUpload = async (file) => {
        Swal.fire("File uploaded");
          uploadFile(file, config)
              .then(data => console.log(data))
              .catch(err => console.error(err))
      }
    return (
        <ServicesContainer id="service">
            <ServicesH1>Claim your amount now</ServicesH1>
            {/* <ServicesWrapper> */}
                 <ServicesCard>
                    <ServicesIcon src={Icon1} />
                     {/*<ServicesH2>Reduce expenses</ServicesH2>
                    <ServicesP>We help reduce your fees and increase your overall revenue.</ServicesP> */} 
                    <div className="row justify-content-center">
                    <input
                            type="file"
                            onChange={handleFileInput}                         
                        />
                        <MDBBtn
                            gradient="aqua" 
                            onClick={() => handleUpload(selectedFile)}
                        >
                                Submit
                        </MDBBtn> 
                    </div>
                </ServicesCard>
            {/* </ServicesWrapper> */}
        </ServicesContainer>
    )
};

export default Service;