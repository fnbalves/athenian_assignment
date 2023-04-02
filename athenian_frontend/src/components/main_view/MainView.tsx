import React, { FC } from 'react';
import CsvUploader from '../csv_uploader/CsvUploader';
import documentStore from '../../stores/document';
import StatisticsPanel from '../statistics_panel/StatisticsPanel';
import Plots from '../plots/Plots';
import axios from 'axios';
import GetShare from '../get_share/GetShare';
import { useLocation } from 'react-router-dom';
import shareStore from '../../stores/share_data';
import CONSTANTS from '../../constants/constants';

interface MainViewProps {

}

const MainView: FC<MainViewProps> = ({}) => {
    const [documentId,setDocumentId] = documentStore(state => [state.documentId, state.setDocumentId]);
    const [latestLoadedUuid, setLatestLoadedUuid] = shareStore(state => [state.latestLoadedUuid, state.setLatestLoadedUuid]);

    const routePath = useLocation()?.pathname?.replace("/", "");
    
    /* The backend endpoints could be made to receive the uuid so we would not expose the id */
    const loadDocumentId = (uuid: string) => {
        const serverUrl = `${CONSTANTS.BACKEND_SERVER}/api/sharing/recover/${uuid}`;
        axios.get(serverUrl).then(res=>{
            const documentId = res?.data?.document_id;
            if (documentId !== undefined && documentId > 0) {
                setDocumentId(documentId);
                setLatestLoadedUuid(uuid);
            }
        });
    }

    if (routePath?.length > 0 && routePath != latestLoadedUuid) {
        loadDocumentId(routePath);
    }

    return (
        <div>
            <h1>File statistics</h1>
            <CsvUploader></CsvUploader>
            {documentId > 0 && <div>
                <GetShare></GetShare>
                <StatisticsPanel></StatisticsPanel>
                <Plots></Plots>
            </div>}
        </div>
    );
}

export default MainView;