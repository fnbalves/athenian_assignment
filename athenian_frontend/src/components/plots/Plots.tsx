import React, { FC } from 'react';
import CONSTANTS from '../../constants/constants';
import axios from 'axios';
import documentStore from '../../stores/document';
import rawDataStore, {RawData} from '../../stores/raw_data';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import './Plots.css';

type PlotsProps = {

}

type DataByTeam = {
    team: string;
    date: Date[];
    review_time: number[];
    merge_time: number[];
}
const Plots: FC<PlotsProps> = ({}) => {
    const [documentId,setDocumentId] = documentStore(state => [state.documentId, state.setDocumentId])
    const [uploadProgress,setUploadProgress] = documentStore(state => [state.uploadProgress, state.setUploadProgress])
    const [isUploading,setIsUploading] = documentStore(state => [state.isUploading, state.setIsUploading])
    const [fileToSend,setFileToSend] = documentStore(state => [state.fileToSend, state.setFileToSend])
    const [status,setStatus] = documentStore(state => [state.status, state.setStatus])
    const [columnsValid,setColumnsValid] = documentStore(state => [state.columnsValid, state.setColumnsValid])
    const [notEmpty,setNotEmpty] = documentStore(state => [state.notEmpty, state.setNotEmpty])

    const [rawData, setRawData] = rawDataStore(state => [state.rawData, state.setRawData]);
    const [latestDocumentId, setLatestDocumentId] = rawDataStore(state => [state.latestDocumentId, state.setLatestDocumentId]);
    
    const getStatistics = (documentId: number) => {
        setLatestDocumentId(documentId);
        const serverUrl = `${CONSTANTS.BACKEND_SERVER}/api/pr_data/${documentId}`;
        axios.get(serverUrl).then(res=>{
            const converted = (res?.data as RawData);
            setRawData(converted);
        });
    }

    if (documentId !== -1 && documentId !== latestDocumentId) {
        // Update data
        setTimeout(() => {getStatistics(documentId)}, 0);
    }

    const getTargetTeam = (teams: DataByTeam[], team_name: string) => {
        const target = teams.filter(t => t.team === team_name);
        if (target?.length > 0) {
            return target[0];
        }
        return null;
    }
    const separateByTeam = () => {
        const dataByTeam: DataByTeam[] = [];
        const numPoints = rawData?.date?.length > 0 ? rawData?.date?.length : 0;
        for(let i = 0; i < numPoints; i++) {
            const team = rawData?.team[i];
            const targetTeam = getTargetTeam(dataByTeam, team);
            if (targetTeam === null) {
                const newTeam = {
                    team: team,
                    date: [rawData?.date[i]],
                    review_time: [rawData?.review_time[i]],
                    merge_time: [rawData?.merge_time[i]]
                }
                dataByTeam.push(newTeam);
            }
            else {
                targetTeam.date.push(rawData?.date[i]);
                targetTeam.review_time.push(rawData?.review_time[i]);
                targetTeam.merge_time.push(rawData?.merge_time[i]);
            }
        }
        return dataByTeam;
    }

    const buildOptionsFromDataByteam = (dataByTeam: DataByTeam[]) => {
        const baseOptions = {
            title: {
                text: ''
            },
            subtitle: {
                text: ''
            },
            series: [],
            yAxis: {
                title: {
                    text: ''
                }
            },
            xAxis: {
                title: {
                    text: 'Date'
                }
            },
            colors: ['#6CF', '#39F', '#06C', '#036', '#000'],
            plotOptions: {
                series: {
                  marker: {
                    enabled: true,
                    radius: 2.5
                  }
                }
            },
        }
        const optionsReview = JSON.parse(JSON.stringify(baseOptions));
        const optionsMerge = JSON.parse(JSON.stringify(baseOptions));
        optionsReview.title.text = 'Review time';
        optionsMerge.title.text = 'Merge time';
        optionsReview.yAxis.title.text = 'Review time';
        optionsMerge.yAxis.title.text = 'Merge time';
        dataByTeam.forEach(team => {
            const date = team.date;
            const review_time = team.review_time;
            const merge_time = team.merge_time;
            const review_time_points = date.map((d, index) => 
                [d, review_time[index]]
            );
            const merge_time_points = date.map((d, index) => 
                [d, merge_time[index]]
            );
            optionsReview.series.push({
                name: `Review time - ${team.team}`,
                data: review_time_points
            });
            optionsMerge.series.push({
                name: `Merge time - ${team.team}`,
                data: merge_time_points
            });
        });
        return {optionsReview, optionsMerge};
    }

    const dataByTeam = separateByTeam();
    const {optionsReview, optionsMerge} = buildOptionsFromDataByteam(dataByTeam);

    return (
        <div>
            <h1>Plots</h1>
            {(rawData?.date?.length > 0) && <div id="charts_container">
                <HighchartsReact
                    highcharts={Highcharts}
                    options={optionsReview}
                />
                <HighchartsReact
                    highcharts={Highcharts}
                    options={optionsMerge}
                />
                </div>
            }
            
        </div>
    )
}

export default Plots;