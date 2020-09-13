import React from 'react';
import { Route, Switch } from 'react-router-dom';
import Home from './Components/Home/Home'

class App extends React.Component {

    render() {
        return(
            <div>
                <Switch>
                    <Route component = { Home } exact path = '/' />
                </Switch>
            </div>
        );
    }
}

export default App;