import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Behavior.css';

const Behavior = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const dog = location.state.dog; // URL에서 state를 통해 전달된 dog 객체를 가져옵니다.

    const [selectedVideo, setSelectedVideo] = useState(null); // 사용자가 선택한 비디오 파일을 저장합니다.
    const [showConfirmationModal, setShowConfirmationModal] = useState(false); // 업로드 확인 모달의 표시 여부를 결정합니다.
    const [uploading, setUploading] = useState(false); // 업로드 중 상태를 나타냅니다.

    // 비디오 파일을 선택할 때 실행될 함수입니다.
    const handleVideoUpload = (event) => {
        setSelectedVideo(event.target.files[0]); // 선택된 파일을 상태에 저장합니다.
        setShowConfirmationModal(true); // 확인 모달을 표시합니다.
    };

    // 비디오 파일을 서버로 업로드하는 함수입니다.
    const uploadVideoToServer = async (file) => {
        setUploading(true); // 업로드 중 상태를 활성화합니다.
        const formData = new FormData();
        formData.append('file', file); // FormData 객체에 파일을 추가합니다.

        try {
            const response = await fetch('/api/upload_video', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Upload successful:', data);
            navigate('/Result', { state: { result: data } }); // 결과 페이지로 이동합니다.
        } catch (error) {
            console.error('Upload failed:', error);
        } finally {
            setUploading(false); // 업로드 중 상태를 비활성화합니다.
        }
    };

    // 업로드를 확인하는 버튼을 클릭했을 때 실행될 함수입니다.
    const handleConfirmUpload = () => {
        if (selectedVideo) {
            uploadVideoToServer(selectedVideo);
        }
        setShowConfirmationModal(false); // 모달을 닫습니다.
        setSelectedVideo(null); // 선택된 비디오를 초기화합니다.
    };

    // 업로드 모달을 닫을 때 실행될 함수입니다.
    const closeConfirmationModal = () => {
        setShowConfirmationModal(false); // 모달을 닫습니다.
        setSelectedVideo(null); // 선택된 비디오를 초기화합니다.
    };

    return (
        <div>
            <header onClick={() => navigate('/Home')}>
                <img alt="dog" src="img/header.png" />
            </header>

            <div className="video-upload">
                <p>{dog.name}의 영상을 업로드 해주세요</p>
                <input id="videoUpload" type="file" accept="video/*" onChange={handleVideoUpload} />
                {selectedVideo && (
                    <div>
                        <video controls width="280">
                            <source src={URL.createObjectURL(selectedVideo)} type="video/mp4" />
                        </video>
                        <button className="uploadbtn" onClick={() => setShowConfirmationModal(true)}>Upload</button>
                    </div>
                )}
            </div>

            {showConfirmationModal && (
                <div className="videoModal">
                    <div className="modal-cont">
                        <p className="first-element"><b>Confirm Upload</b></p>
                        <p className="first-element">Do you want to upload the selected video?</p>
                        <div className='confirmBtn'>
                            <button className="second-element" onClick={handleConfirmUpload}>Yes</button>
                            <button className="third-element" onClick={closeConfirmationModal}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

            {uploading && <div>Uploading...</div>}
        </div>
    );
};

export default Behavior;
