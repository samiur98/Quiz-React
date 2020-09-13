import React from 'react';
import "./Home.css";

function Header(props) {
    return (
        <div className = 'home-header'>
            <h1>QUIZ REACT</h1>
            <input 
            type='text' 
            placeholder = 'Search for Fun Quizzes'
            />
            <button>Search</button>
        </div>
    );
}

function OptionsMenu(props) {
    return(
        <div className = 'home-options'>
            <p>Add Quiz</p>
            <p>Sign In</p>
            <p>Sign Up</p>
        </div>
    );
}

function SampleQuizzes(props) {
    return(
        <div className = 'home-sample'>
            <h1>Try out some of these Sample Quizzes</h1>
            <div className = 'home-sample-container'>
                
            </div>
        </div>
    );
}

function HomeView(props) {
    return(
        <div>
            <Header />
            <OptionsMenu />
            <SampleQuizzes />
        </div>
    );
}

export default HomeView;