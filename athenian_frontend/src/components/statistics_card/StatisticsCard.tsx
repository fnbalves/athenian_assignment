import './StatisticsCard.css';
import React, { FC } from 'react';

type StatisticsCardProps = {
    statsName: string;
    meanVal: number;
    maxVal: number;
    minVal: number;
    stdVal: number;
    medianVal: number;
}

const StatisticsCard: FC<StatisticsCardProps> = (props: StatisticsCardProps) => {
    return (
        <div id="statistics_card">
            <p className="stats_name">{props.statsName}</p>
            <p className="stats">Mean: {props.meanVal.toFixed(2)}</p>
            <p className="stats">Max: {props.maxVal.toFixed(2)}</p>
            <p className="stats">Min: {props.minVal.toFixed(2)}</p>
            <p className="stats">Std: {props.stdVal.toFixed(2)}</p>
            <p className="stats">Median: {props.medianVal.toFixed(2)}</p>
        </div>
    )
}

export default StatisticsCard;