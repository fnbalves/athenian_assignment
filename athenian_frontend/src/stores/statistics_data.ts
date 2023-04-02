import create from 'zustand'

export type ColumnStatistics = {
    mean_val: number,
    max_val: number,
    min_val: number,
    std_val: number,
    median_val: number
}

export type TeamStatistics = {
    team_name: string,
    review_time: ColumnStatistics,
    merge_time: ColumnStatistics
}

export type StatisticsState = {
    statistics: TeamStatistics[],
    latestDocumentId: number,
    setStatistics: (statistics: TeamStatistics[]) => void;
    setLatestDocumentId: (latestDocumentId: number) => void;
}

const statisticsStore = create<StatisticsState>((set) => ({
    statistics: [],
    latestDocumentId: -1,
    setStatistics: (new_stats: TeamStatistics[]) => {
        set(state => ({statistics: new_stats}))
    },
    setLatestDocumentId: (latestDocumentId: number) => {
        set(state =>({latestDocumentId: latestDocumentId}))
    },
}));

export default statisticsStore;