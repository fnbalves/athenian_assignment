import create from 'zustand'

export type ShareState = {
    uuid: string,
    latestLoadedUuid: string,
    setUuid: (uuid: string) => void,
    setLatestLoadedUuid: (latestLoadedUuid: string) => void;
}

const shareStore = create<ShareState>((set) => (
    {
        uuid: '',
        latestLoadedUuid: '',
        setUuid: (uuid: string) => {
            set(state => ({uuid: uuid}))
        },
        setLatestLoadedUuid: (latestLoadedUuid: string) => {
            set(state => ({latestLoadedUuid: latestLoadedUuid}))
        } 
    }
))

export default shareStore;