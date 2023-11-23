import './Result.css';
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const Result = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const dog = location.state?.dog;
    const resultObj = location.state?.result; // 서버로부터 받은 결과 객체
    const resultText = resultObj ? resultObj.result : null; // 결과 객체에서 텍스트 추출

    const handletitleClick = () => {
        navigate('/Home');
    }

    return (
        <div>
            <header> <img onClick={handletitleClick} alt="dog" src="img/header.png" /></header>
            {dog ? (
                <div>
                    <h3>강아지 정보</h3>
                    <p>이름: {dog.dog.name}</p>
                    <p>나이: {dog.dog.age}</p>
                    <p>성별: {dog.dog.gender}</p>
                    <p>품종: {dog.dog.breed}</p>
                </div>
            ) : resultText ? (
                <div>
                    <h3>분석 결과</h3>
                    <p>{resultText}</p>
                </div>
            ) : (
                <div>
                    <h3>결과 없음</h3>
                    <p>업로드한 파일의 분석 결과가 없습니다.</p>
                </div>
            )}
        </div>
    );
};

export default Result;
