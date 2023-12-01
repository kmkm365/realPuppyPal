import './Result.css';
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const Result = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const dog = location.state?.dog;
    const resultObj = location.state?.result; // 서버로부터 받은 결과 객체
    const resultText = resultObj ? resultObj.result : null; // 결과 객체에서 텍스트 추출
    const selectedVideo = location.state?.selectedVideo;
    const handletitleClick = () => {
        navigate('/Home');
    }

    const resultdata = '<분석 결과>';
    return (
        <div>
            <header onClick={handletitleClick} > <img alt="dog" src="img/header.png" /></header>

            <div className='result-box'>
                <div className='dogInfo'>
                    <video controls width="280">
                        <source src={URL.createObjectURL(selectedVideo)} type="video/mp4" />
                    </video>
                    {dog ? (<div className='dogInfo-details'>
                        <p>이름 : {dog.name}</p>
                        <p>나이 : {dog.age}</p>
                        <p>성별 : {dog.gender}</p>
                        <p>품종 : {dog.breed}</p>
                    </div>) : (<></>)}

                </div>
                <div className='stateInfo'>
                    <h3>{resultdata}</h3>
                    <img src="img/sleep.png"></img>
                    {dog ? (<p>
                        상태: {dog.name}(이)는 지금 졸려요..
                    </p>) : (<p>
                        상태: 졸려요..
                    </p>)}
                    <p>{resultText}</p>
                </div>
            </div>

        </div>
    );
};

export default Result;