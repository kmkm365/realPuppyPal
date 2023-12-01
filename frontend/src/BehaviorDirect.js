import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './BehaviorDirect.css';

const BehaviorDirect = () => {
    const navigate = useNavigate();
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [showConfirmationModal, setShowConfirmationModal] = useState(false);
    const [uploading, setUploading] = useState(false);

    const handleVideoUpload = (event) => {
        setSelectedVideo(event.target.files[0]);
    };
    const handleConfirmUpload = () => {
        if (selectedVideo) {
            setShowConfirmationModal(true);
        }
    };

    const closeConfirmationModal = () => {
        setShowConfirmationModal(false);
        setSelectedVideo(null);
    };

    const uploadVideoToServer = async (file) => {
        const formData = new FormData();
        formData.append('file', file);

        const tryUploadToLocalServer = async () => {
            const response = await fetch('/api/upload', {
                method: 'POST',
                mode: 'cors',
                body: formData,
            });
            return response;
        };

        const tryUploadToCloudServer = async () => {
            const response = await fetch('/cloudapi/upload', {
                method: 'POST',
                mode: 'cors',
                body: formData,
            });
            return response;
        };

        try {
            setUploading(true);

            let response = await tryUploadToLocalServer();

            if (!response.ok) {
                console.error('Upload to local server failed, trying cloud server');
                response = await tryUploadToCloudServer();
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Upload successful:', data);
            navigate('/Result', { state: { result: data, selectedVideo: selectedVideo } });
        } catch (error) {
            console.error('Upload failed:', error);
            alert('Upload failed');
        } finally {
            setUploading(false);
            setShowConfirmationModal(false);
            setSelectedVideo(null);
        }
    };

    return (
        <div>
            <header onClick={() => navigate('/Home')}>
                <img alt="dog" src="img/header.png" />
            </header>

            <div className="video-upload">
                <p>영상을 업로드 해주세요</p>
                <input id="videoUpload" type="file" accept="video/*" onChange={handleVideoUpload} />
                {selectedVideo && (
                    <div>
                        <video controls width="280">
                            <source src={URL.createObjectURL(selectedVideo)} type="video/mp4" />
                        </video>
                        <button className="uploadbtn" onClick={handleConfirmUpload}>
                            Upload
                        </button>
                    </div>
                )}
            </div>

            {showConfirmationModal && (
                <div className="videoModal">
                    <div className="modal-cont">
                        <p className="first-element">
                            <b>업로드 확인</b>
                        </p>
                        <p className="first-element">Do you want to upload the selected video?</p>
                        <div className="confirmBtn">
                            {uploading ? (
                                <div>
                                    <p className='loading'>loading..</p>
                                    <div className="loading-spinner"></div>
                                </div>


                            ) : (

                                <>
                                    <button className="second-element" onClick={() => uploadVideoToServer(selectedVideo)}>
                                        Yes
                                    </button>
                                    <button className="third-element" onClick={() => closeConfirmationModal()}>
                                        Cancel
                                    </button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BehaviorDirect;
