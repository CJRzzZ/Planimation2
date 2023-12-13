import React from "react";
import {subGoal, stepInfo, allStages, steps, stepSubgoalMap, vfg, textContent,
        getAllStages, getSteps, getStepInfo, getSubGoal, getStepSubgoalMap} from './dataUtils';
import Button from '@material-ui/core/Button';
import styles from './index.less';
import Screen, { ControlPanel, StepScreen, GoalScreen, SplitButton } from "./screenComponents";


import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import TextField from '@mui/material/TextField';
import DialogActions from '@mui/material/DialogActions';

import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

import {
    FormControl,
    RadioGroup,
    FormControlLabel,
    Radio
} from '@material-ui/core';

import CircularProgress from "@material-ui/core/CircularProgress";

import Select from '@mui/material/Select';

import { InputLabel } from '@material-ui/core';

class mediaDataLabel {

    constructor(fileType = 'vfg', startStep = 0, stopStep = 1, quality = "high") {
        this.fileType = fileType;
        this.startStep = startStep;
        this.stopStep = stopStep;
        this.quality = quality;
    }
    bodyContent() {
        const bodyContent = {
            'fileType': this.fileType,
            'startStep': this.startStep,
            'stopStep': this.stopStep,
            'quality': this.quality
        }
        return bodyContent;
    }
}

class PageFour extends React.Component {

    constructor(props) {
        super(props);
        
        this.stepItem = {};
        steps.forEach((step, i) => {
            this.stepItem[i] = React.createRef();
        })


        this.state = {
            // data that will be used/changed in render function
            stageIndex: 0,
            stepInfoIndex: 0,
            showKey: '',
            showPlayButton: true,
            selectedSubGoals: {},
            drawSprites: allStages[0],
            playSpeed: 3,
            playButtonColor: 'primary',
            pauseButtonColor: 'default',
            canvasWidth: 720,
            canvasHeight: 470,
            radioOption: 'all', 
            currentDialogType: null,
            isLoading: false,
            qualityOption: 'medium',
        }

        // Every function that interfaces with UI and data used
        // in this class needs to bind like this:
        this.handleOnClick = this.handleOnClick.bind(this);
        this.updateWindowDimensions = this.updateWindowDimensions.bind(this);
        this.handleMenuOpen = this.handleMenuOpen.bind(this);
        this.handleMenuClose = this.handleMenuClose.bind(this);
        this.handleOpenDialog = this.handleOpenDialog.bind(this);
        this.handleCloseDialog = this.handleCloseDialog.bind(this);
        this.handleNumberChange = this.handleNumberChange.bind(this);
    }

    

    updateWindowDimensions() {
            const clientWidth = window.document.clientWidth || window.innerWidth || window.document.body.clientWidth;
            const clientHeight = window.document.clientHeight || window.innerHeight || window.document.body.clientHeight;
            
            // when the window is loaded at the backgroud, the clientwidth will be set to 0.
            if (clientWidth !=0){
                const tmp_width = Math.max(clientWidth - 550, 400);
                this.setState({ canvasWidth: tmp_width, canvasHeight: Math.min(tmp_width / 2, clientHeight - 120)  },(val)=>{
                    // console.log('client.inner',clientWidth, clientHeight);
                });
        }
        
    }



    handleOnClick() {
        this.props.history.push('/');
    
    }



    handleSubItemClick = (key) => {
        // this.state.stageIndex = index;
        if(this.state.showKey !== key) {
            this.setState({
                showKey: key,
            });
        } else {
            this.setState({
                showKey: "",
            });
        }
    }



    componentDidMount() {
     
        this.updateWindowDimensions();
        window.addEventListener('resize', this.updateWindowDimensions);
        
    }





    /**
     * Change the style of the highlighted subgoal
     * @param {Integer} index 
     * @returns 
     */
    highlight(index) {
        const highlightSubGoals = stepSubgoalMap.get(index) || [];
        const map = {};
        highlightSubGoals.forEach(item => {
            map[item]=true;
        });
        return map;
    }


    /**
     * Calculate and diplays interpolation animation between two stages
     * @param {Integer} index 
     */
    animation(index) {
        // 2 sets of sprites
        const previousStageIndex = this.state.stageIndex;
        const previousStage = allStages[previousStageIndex];
        const newStage = allStages[index];
        const times = 20;
        newStage.sort((itemA, itemB) => itemA.depth - itemB.depth);


        const movedSprites = {};
        previousStage.map((eachSprite, i) => {
            if(eachSprite.name !== newStage[i].name) return
            if(eachSprite.x !== newStage[i].x || eachSprite.y !== newStage[i].y) {
                const changingPos = [];
                for (let j = 0; j < times; j++) {
                    const specificPos = {}

                    specificPos.minX = eachSprite.minX + (newStage[i].minX - eachSprite.minX)/times * (j + 1);
                    specificPos.maxX = eachSprite.maxX + (newStage[i].maxX - eachSprite.maxX)/times * (j + 1);
                    specificPos.minY = eachSprite.minY + (newStage[i].minY - eachSprite.minY)/times * (j + 1);
                    specificPos.maxY = eachSprite.maxY + (newStage[i].maxY - eachSprite.maxY)/times * (j + 1);
                    changingPos.push(specificPos)
                }
                movedSprites[eachSprite.name] = changingPos
            }
        })

        // draw 100 times, during 2 seconds, slash: 20ms
        let i = 0;
        if(this.handler) {
            clearInterval(this.handler);
        }
        const handler = setInterval(()=>{
            const newDrawSprites = previousStage.map( sprite => {
                // sprite -> sprite.id
                if(movedSprites[sprite.name]) {
                    const move = movedSprites[sprite.name];
                    // I need to move
                    // Replace old x, y, with computed x, y (which will change per 20ms)
                    // return sprite;

                    return {
                        ...sprite,
                        minX: move[i].minX,
                        maxX: move[i].maxX,
                        maxY: move[i].maxY,
                        minY: move[i].minY
                    };
                } else {
                    // Keep at original position
                    return sprite;
                }
            })

            this.setState({
                drawSprites: [...newDrawSprites]
            });
            i++;

            if( i >= times){
                clearInterval(handler);
                this.handler = false;
                this.setState({
                    drawSprites: [...newStage]
                });
            }
        }, 60/this.state.playSpeed);
        this.handler = handler;
    };



    handleStepsClick = (index) =>{
        // Get Stage[index] sprites, and display
        if(this.handlerPlay) {
            clearInterval(this.handlerPlay);
        }
        this.animation(index)
        const map = this.highlight(index)

        this.setState({
            stageIndex: index,
            stepInfoIndex: index,
            selectedSubGoals: map,
            playButtonColor: 'primary',
            pauseButtonColor: 'default'
        });
        this.animation(index)
    }



    handleSubgoalStepItemClick = (value) => {
        if(this.handlerPlay) {
            clearInterval(this.handlerPlay);
        }
        const index = Number(value);

        this.animation(index)
        const map = this.highlight(index)

        this.setState({
            stageIndex: index,
            stepInfoIndex: index,
            selectedSubGoals: map,
            playButtonColor: 'primary',
            pauseButtonColor: 'default'
        });
        this.animation(index)
        this.stepItem[index].current.scrollIntoView();
    }



    handlePreviousClick = (value) => {
        const previousIndex = Number(value) - 1;
        if (previousIndex < 0) {
            alert("It's already the initial state!")
        }
        else{
            this.animation(previousIndex)
            const map = this.highlight(previousIndex)
            this.setState({
                stageIndex: previousIndex,
                stepInfoIndex: previousIndex,
                selectedSubGoals: map
            });
            this.animation(previousIndex)
            this.stepItem[previousIndex].current.scrollIntoView();
        }
    }



    handleNextClick = (value) => {
        const nextIndex = Number(value) + 1
        if (nextIndex >= steps.length) {
            alert("It's already the final state!")
        }
        else{
            this.animation(nextIndex)
            const map = this.highlight(nextIndex)
            this.setState({
                stageIndex: nextIndex,
                stepInfoIndex: nextIndex,
                selectedSubGoals: map
            });
            this.animation(nextIndex)
            this.stepItem[nextIndex].current.scrollIntoView();
        }
    }



    handleStartClick = (value) => {
        let nextIndex = Number(value) + 1
        if(nextIndex === steps.length) {
            alert("It's already the final state!")
        } else {
            const map = this.highlight(nextIndex)
            this.setState({
                stageIndex: nextIndex,
                stepInfoIndex: nextIndex,
                selectedSubGoals: map,
                playButtonColor: 'default',
                pauseButtonColor: 'primary'}
            )
            this.animation(nextIndex)
            this.stepItem[nextIndex].current.scrollIntoView();

            nextIndex++;
            if(this.handlerPlay) {
                clearInterval(this.handlerPlay);
            }
            if(steps.length > nextIndex) {
                const run = () => {
                    const map = this.highlight(nextIndex)
                    this.animation(nextIndex)
                    this.setState({
                        stageIndex: nextIndex,
                        stepInfoIndex: nextIndex,
                        selectedSubGoals: map
                    })
                    this.stepItem[nextIndex].current.scrollIntoView();

                    nextIndex++;

                    if (nextIndex >= steps.length) {
                        if(this.handlerPlay) {
                            clearTimeout(this.handlerPlay);
                        }
                        this.setState({
                            playButtonColor: 'primary',
                            pauseButtonColor: 'default'}
                        )
                    } else {
                        // setInterval effect
                        // detect change of playSpeed
                        const handlerPlay = setTimeout(run, 2700/this.state.playSpeed);
                        this.handlerPlay = handlerPlay;
                    }
                };

                const handlerPlay = setTimeout(run, 2700/this.state.playSpeed);
                this.handlerPlay = handlerPlay;
            }
        }
    }



    handlePauseClick = () => {
        if(this.handlerPlay) {
            this.setState( {
                playButtonColor: 'primary',
                pauseButtonColor: 'default'
            })
            clearInterval(this.handlerPlay);
        }
    }



    handleResetClick = () => {
        if(this.handlerPlay) {
            clearInterval(this.handlerPlay);
        }
        this.animation(0)
        const map = this.highlight(0)
        this.setState( {
            stageIndex: 0,
            stepInfoIndex: 0,
            selectedSubGoals: map,
            playButtonColor: 'primary',
            pauseButtonColor: 'default'
        })
        this.stepItem[0].current.scrollIntoView();
    }



    handleShowFinalGoalClick = () =>{
        if(this.handlerPlay) {
            clearInterval(this.handlerPlay);
        }
        const index = Number(steps.length) - 1;
        this.animation(index)
        const map = this.highlight(index)
        this.setState( {
            stageIndex: index,
            stepInfoIndex: index,
            selectedSubGoals: map,
            playButtonColor: 'primary',
            pauseButtonColor: 'default'
        })
        this.stepItem[index].current.scrollIntoView();
    }



    handleExportClick = () =>{
        const data = textContent
        let blob = new Blob([data]);
        let filename = "download.vfg";

        if (typeof window.navigator.msSaveBlob !== "undefined") {
            window.navigator.msSaveBlob(blob, filename);
        } else {
            var blobURL = window.URL.createObjectURL(blob);
            // create a hidden <a> tag for download
            var tempLink = document.createElement("a");
            tempLink.style.display = "none";
            tempLink.href = blobURL;
            tempLink.setAttribute("download", filename);
            if (typeof tempLink.download === "undefined") {
                tempLink.setAttribute("target", "_blank");
            }
            document.body.appendChild(tempLink);
            tempLink.click();
            document.body.removeChild(tempLink);
            window.URL.revokeObjectURL(blobURL);
        }
    }


    async sendMediaRequestAndDownload(fileType, startStep, stopStep, qualityOption) {
        try {
          const vfgText = JSON.stringify(vfg);
          //console.log(vfgText);
          var label = new mediaDataLabel();
          // assign any parameters here. otherwise, default will be used.
          label.fileType = fileType;
          switch (fileType){
            case "mp4":
                label.startStep = startStep;
                label.stopStep = stopStep;
                label.quality = qualityOption;
                break;
            case "png":
                label.startStep = startStep;
                label.stopStep = stopStep;
                break;
            case "gif":
                label.startStep = startStep;
                label.stopStep = stopStep;
                label.quality = qualityOption;
                break;
          }

          const requestData = {
            method: 'POST',
            body: JSON.stringify({
              'vfg': vfgText,
              'fileType': fileType,
              'params': label.bodyContent()
            })
          };
    
          // For local testing, uncomment the next line and comment the following line.
          //const response = await fetch("http://localhost:8000/downloadVisualisation", requestData);
          const response = await fetch("https://planimation.planning.domains/downloadVisualisation", requestData);

          if (response.ok) {
            console.log("Response was OK");
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            if (fileType == "png"){
                fileType = "zip";
            }
            a.download = 'planimation.'+fileType;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
          } else {
            console.error("Failed to download the file.");
          }
        } catch (error) {
          console.error("Error:", error);
        }
      }

      
      // this function is for testing @Wenxuan
      async handleMediaButtonClick(fileType) {
          try {
    
            this.sendMediaRequestAndDownload(fileType);
            
          } catch(err) {
              console.error("There was an error: ", err);
          }
 
    
    }


    handleSpeedControllor = (value) => {
        this.setState({
            playSpeed: value
        });
    };

    
    /**
     * prevent crash when jumping  to other pages during the animation playing
     *  */
    componentWillUnmount(){
        if(this.handlerPlay) {
            clearInterval(this.handlerPlay);
        }
        window.removeEventListener('resize', this.updateWindowDimensions);
        
    }


    handleMenuOpen = (event) => {
        this.setState({ anchorEl: event.currentTarget });
    };

    handleMenuClose = () => {
        this.setState({ anchorEl: null });
    };

    handleOpenDialog = (type) => {
        this.setState({ 
            isModalOpen: true,
            currentDialogType: type
        });
    }
    
    
    handleCloseDialog = () => {
        this.setState({ isModalOpen: false });
    }
    
    handleNumberChange = (e, numberIndex) => {
        this.setState({ [numberIndex]: e.target.value });
    }

    handleRadioChange = (event) => {
        this.setState({
            radioOption: event.target.value
        });
    }


    handleDownload = async () => {
        this.setState({ isloading: true });
        if (this.state.radioOption === 'all') {
            await this.sendMediaRequestAndDownload(this.state.currentDialogType, 0, 9999, this.state.qualityOption);
        } else {
            const { number1, number2 } = this.state;
            await this.sendMediaRequestAndDownload(this.state.currentDialogType, number1, number2, this.state.qualityOption);
        }
        this.handleCloseDialog();
        setTimeout(() => {
            this.setState({ isloading: false });
        }, 2000);
    }

    handleQualityChange = (event) => {
        this.setState({ qualityOption: event.target.value });
    };
    



    render() {
        // Get all sprites
        let sprites = this.state.drawSprites;
        // Sort sprites by their depth
        sprites && sprites.sort((itemA, itemB) => itemA.depth - itemB.depth);
    
        return (
            <div className={styles.container} ref={(ref) => this.refDom = ref}>
                <div className={styles.left}>
                    <StepScreen stepInfoIndex={this.state.stepInfoIndex} stepItem={this.stepItem} stepInfo={stepInfo} onStepClick={this.handleStepsClick} />
                </div>
                <div className={styles.middle}>
                    <Screen canvasWidth={this.state.canvasWidth} canvasHeight={this.state.canvasHeight} sprites={this.state.drawSprites} vfg={vfg} />
                    <div className={styles.btn_box}>
                        <div>
                            <ControlPanel
                                playButtonColor={this.state.playButtonColor}
                                pauseButtonColor={this.state.pauseButtonColor}
                                stepInfoIndex={this.state.stepInfoIndex}
                                onPreviousClick={this.handlePreviousClick}
                                onStartClick={this.handleStartClick}
                                onPauseClick={this.handlePauseClick}
                                onNextClick={this.handleNextClick}
                                onResetClick={this.handleResetClick}
                                onSpeedControllor={this.handleSpeedControllor}>
                            </ControlPanel>
                        </div>
                    </div>
                </div>
    
                <div className={styles.right}>
                    <div style={{ marginTop: '5px', marginBottom: '5px', width: '220px' }}>
                        <Button variant="contained" color="primary" size="small" onClick={() => { this.handleShowFinalGoalClick() }}>
                            Show the Goal
                        </Button>
                        &nbsp;&nbsp;
                        <Button variant="contained" color="primary" size="small" onClick={this.handleMenuOpen}>
                            Export
                        </Button>
                        {this.state.isloading && <CircularProgress size={24} />}
                        <Menu
                            anchorEl={this.state.anchorEl}
                            open={Boolean(this.state.anchorEl)}
                            onClose={this.handleMenuClose}
                        >
                            <MenuItem onClick={() => { this.handleExportClick(); this.handleMenuClose(); }}>
                                Export .vfg
                            </MenuItem>
                            <MenuItem onClick={() => { this.handleOpenDialog("png"); this.handleMenuClose(); }}>
                                Export .png
                            </MenuItem>
                            <MenuItem onClick={() => { this.handleOpenDialog("gif"); this.handleMenuClose(); }}>
                                Export .gif
                            </MenuItem>
                            <MenuItem onClick={() => { this.handleOpenDialog("mp4"); this.handleMenuClose(); }}>
                                Export .mp4
                            </MenuItem>
                        </Menu>
                        <Dialog open={this.state.isModalOpen} onClose={this.handleCloseDialog}>
                            <DialogTitle>Download as {this.state.currentDialogType}</DialogTitle>
                            <DialogContent>
                                <FormControl component="fieldset">
                                    <RadioGroup
                                        value={this.state.radioOption}
                                        onChange={this.handleRadioChange}
                                    >
                                        <FormControlLabel
                                            value="all"
                                            control={<Radio />}
                                            label="Download All"
                                        />
                                        <FormControlLabel
                                            value="range"
                                            control={<Radio />}
                                            label="Specify range"
                                        />
                                    </RadioGroup>
                                </FormControl>
                                {/* No need for quality option for PNGs */}
                               
    
                                {this.state.radioOption === 'range' && (
                                    <>
                                        <div><small>Please enter a step range within 0 and {Number(steps.length) - 1}.</small></div>
                                        <TextField
                                            autoFocus
                                            margin="dense"
                                            id="number1"
                                            label="start"
                                            type="number"
                                            fullWidth
                                            value={this.state.number1}
                                            onChange={(e) => this.handleNumberChange(e, 'number1')}
                                        />
                                        <TextField
                                            margin="dense"
                                            id="number2"
                                            label="end"
                                            type="number"
                                            fullWidth
                                            value={this.state.number2}
                                            onChange={(e) => this.handleNumberChange(e, 'number2')}
                                        />
                                    </>
                                )}
                                 {this.state.currentDialogType !== "png" && (
                                    <>
                                        <FormControl fullWidth>
                                            <InputLabel id="quality-label">Quality</InputLabel>
                                            <Select
                                                labelId="quality-label"
                                                value={this.state.qualityOption}
                                                onChange={this.handleQualityChange}
                                            >
                                                <MenuItem value="low">Low</MenuItem>
                                                <MenuItem value="medium">Medium</MenuItem>
                                                <MenuItem value="high">High</MenuItem>
                                            </Select>
                                        </FormControl>
                                    </>
                                )}
                            </DialogContent>
                            <DialogActions>
                                <Button onClick={this.handleCloseDialog} color="primary">Cancel</Button>
                                <Button onClick={this.handleDownload} color="primary">Confirm</Button>
                            </DialogActions>
                        </Dialog>
                    </div>
                    <GoalScreen sprites={sprites} subGoal={subGoal} selectedSubGoals={this.state.selectedSubGoals}
                        showKey={this.state.showKey} onSubItemClick={this.handleSubItemClick} onSubgoalStepItemClick={this.handleSubgoalStepItemClick} />
                </div>
            </div>
        );
    }
}    
export default PageFour;