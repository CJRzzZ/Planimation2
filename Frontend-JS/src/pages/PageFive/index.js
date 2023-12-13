import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import css from '../../Styles/index.module.less';


class PageFive extends React.Component {
    constructor(props) {
        super(props);
        this.receiveMessageFromPlugin = this.receiveMessageFromPlugin.bind(this);
    }
    componentDidMount() {
        localStorage.removeItem('fileContent');
         window.addEventListener('message', this.receiveMessageFromPlugin);
         window.parent.postMessage({"action":"loadfile"}, "*"); 
    }
    componentWillUnmount(){
        window.removeEventListener('message', this.receiveMessageFromPlugin);
    }
    handleStore = (content)=> {
        localStorage.setItem('fileContent', content);
        window.location.href = '/demo';
    }


    async receiveMessageFromPlugin ( event ) {
        if(event.data.domain){
            const formData = new FormData();
            for (const name in event.data) {
              formData.append(name, event.data[name]);
            }
            try {
        
              const resp = await fetch(
                "https://planimation.planning.domains/upload/pddl",
                {
                  //"http://127.0.0.1:8000/upload/pddl" On local server
                  method: "POST", //DO NOT use headers
                  body: formData, // Dataformat
                }
              );
              const data = await resp.json();
              const txt = JSON.stringify(data);
              this.handleStore(txt);
            } catch (error) {
              console.log(error);
              
            } finally {
            }
     
          }
    }


    render() {
        const useStyles = makeStyles((theme) => ({
            root: {
              '& > *': {
                margin: theme.spacing(1),
                width: '25ch',
              },
            },         
          }));

        return (
            <div className={css.container}>
                Loading...  
            </div>
          );
    }
    
  }
  
  export default PageFive;