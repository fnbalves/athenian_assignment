import React, { FC } from 'react';
import './StatisticsPanel.css';
import documentStore from '../../stores/document';
import statisticsStore, {ColumnStatistics, TeamStatistics} from '../../stores/statistics_data';
import CONSTANTS from '../../constants/constants';
import axios from 'axios';
import StatisticsCard from '../statistics_card/StatisticsCard';

type StatisticsPanelProps = {

}

const StatisticsPanel: FC<StatisticsPanelProps> = ({}) => {
    const [documentId,setDocumentId] = documentStore(state => [state.documentId, state.setDocumentId])
    const [uploadProgress,setUploadProgress] = documentStore(state => [state.uploadProgress, state.setUploadProgress])
    const [isUploading,setIsUploading] = documentStore(state => [state.isUploading, state.setIsUploading])
    const [fileToSend,setFileToSend] = documentStore(state => [state.fileToSend, state.setFileToSend])
    const [status,setStatus] = documentStore(state => [state.status, state.setStatus])
    const [columnsValid,setColumnsValid] = documentStore(state => [state.columnsValid, state.setColumnsValid])
    const [notEmpty,setNotEmpty] = documentStore(state => [state.notEmpty, state.setNotEmpty])

    const [statisticData, setStatisticData] = statisticsStore(state => [state.statistics, state.setStatistics]);
    const [latestDocumentId, setLatestDocumentId] = statisticsStore(state => [state.latestDocumentId, state.setLatestDocumentId]);
    
    const getStatistics = (documentId: number) => {
        setLatestDocumentId(documentId);
        const serverUrl = `${CONSTANTS.BACKEND_SERVER}/api/statistics/${documentId}`;
        axios.get(serverUrl).then(res=>{
            const converted = (res?.data as TeamStatistics[]);
            setStatisticData(converted);
        });
    }

    if (documentId !== -1 && documentId !== latestDocumentId) {
        // Update statistics
        setTimeout(() => {getStatistics(documentId)}, 0);
    }

    const separateByTeam = () => {
        let forAll: TeamStatistics = {team_name: "", review_time: {
                mean_val: 0,
                max_val: 0,
                min_val: 0,
                std_val: 0,
                median_val: 0
            },
            merge_time: {
                mean_val: 0,
                max_val: 0,
                min_val: 0,
                std_val: 0,
                median_val: 0
            }
        };
        const teams: TeamStatistics[] = [];
        let hasData = statisticData?.length > 0;
        statisticData?.forEach(s => {
            if (s?.team_name == 'all_data') {
                forAll = s;
            } else {
                teams.push(s);
            }
        })
        return {hasData, forAll, teams};
    }

    let {hasData, forAll, teams} = separateByTeam();

    return (
        <div>
            <h1>Statistics</h1>
            {hasData &&
            <div id="all_statistics">
                <div>
                <p id="team_name">All data</p>
                <div id="all_data_holder">
                    <StatisticsCard
                    statsName="review_time"
                    meanVal={forAll?.review_time.mean_val}
                    maxVal={forAll?.review_time.max_val}
                    minVal={forAll?.review_time.min_val}
                    stdVal={forAll?.review_time.std_val}
                    medianVal={forAll?.review_time.median_val}
                    ></StatisticsCard>

                    <StatisticsCard
                    statsName="merge_time"
                    meanVal={forAll?.merge_time.mean_val}
                    maxVal={forAll?.merge_time.max_val}
                    minVal={forAll?.merge_time.min_val}
                    stdVal={forAll?.merge_time.std_val}
                    medianVal={forAll?.merge_time.median_val}
                    ></StatisticsCard>
                </div>
                </div>
            </div>}
            <div id="by_team">
                {teams.map(t => (
                    <div id="team_holder" key={t.team_name}>
                        <p id="team_name">{t.team_name}</p>
                        <div id="team_data_holder">
                        <StatisticsCard
                        statsName="review_time"
                        meanVal={t?.review_time.mean_val}
                        maxVal={t?.review_time.max_val}
                        minVal={t?.review_time.min_val}
                        stdVal={t?.review_time.std_val}
                        medianVal={t?.review_time.median_val}
                        ></StatisticsCard>

                        <StatisticsCard
                        statsName="merge_time"
                        meanVal={t?.merge_time.mean_val}
                        maxVal={t?.merge_time.max_val}
                        minVal={t?.merge_time.min_val}
                        stdVal={t?.merge_time.std_val}
                        medianVal={t?.merge_time.median_val}
                        ></StatisticsCard>
                        </div>
                    </div>
                    ))
                }
            </div>
        </div>
    );
}

export default StatisticsPanel;

