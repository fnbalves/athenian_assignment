import React, { FC } from 'react';
import CONSTANTS from '../../constants/constants';
import axios from 'axios';
import documentStore from '../../stores/document';
import shareStore from '../../stores/share_data';
import './GetShare.css';

type GetShareProps = {

}

const GetShare: FC<GetShareProps> = ({}) => {
    const [documentId,setDocumentId] = documentStore(state => [state.documentId, state.setDocumentId])
    const [uuid, setUuid] = shareStore(state => [state.uuid, state.setUuid]);    
    
    const getUuid = () => {
        console.log('Getting uuid');
        const serverUrl = `${CONSTANTS.BACKEND_SERVER}/api/sharing/create/${documentId}`;
        axios.post(serverUrl).then(res=>{
            const uuid = res?.data?.uuid;
            console.log('GOT', res, uuid);
            if (uuid !== undefined) {
                setUuid(uuid);
            }
        });
    };

    return (
        <div>
            <h1>Share</h1>
            <div id="share_info">
                {documentId > 0 && <button onClick={getUuid}>Get share url</button>}
                {(uuid !== undefined && uuid !== '') && <p>
                    In order to share this information, share the url: <a href={`${window.location}${uuid}`}>{`${window.location}${uuid}`}</a>    
                </p>}
            </div>
        </div>
    )
}

export default GetShare;