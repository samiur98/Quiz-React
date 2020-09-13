import React from 'react';
import HomeView from './HomeView';

class Home extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            signedIn: false,
            userData: {},
            sampleQuizzes: []
        }
        console.log(this.state);
    }

    render() {
        return(
        <div>
            <HomeView />
        </div>
        );
        
    }
}

export default Home;