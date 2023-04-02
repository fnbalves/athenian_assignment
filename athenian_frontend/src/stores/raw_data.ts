import create from 'zustand'

export type RawData = {
    date: Date[],
    team: string[],
    review_time: number[],
    merge_time: number[]
}

export type RawDataState = {
    rawData: RawData,
    latestDocumentId: number;
    setRawData: (data: RawData) => void;
    setLatestDocumentId: (latestDocumentId: number) => void;
}

const rawDataStore = create<RawDataState>((set) => (
    {
        rawData: {date: [], team: [], review_time: [], merge_time: []},
        latestDocumentId: -1,
        setRawData: (data: RawData) => {
            set(state => ({rawData: data}))
        },
        setLatestDocumentId: (latestDocumentId: number) => {
            set(state => ({latestDocumentId: latestDocumentId}))
        }
    }
));

export default rawDataStore;