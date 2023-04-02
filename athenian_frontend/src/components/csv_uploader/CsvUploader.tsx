import React, { FC } from 'react';
import CONSTANTS from '../../constants/constants';
import axios from 'axios';
import documentStore from '../../stores/document';
import './CsvUploader.css';

type CsvUploaderProps = {
}

const NO_FILE = 'No file selected';
const INCORRECT_TYPE = 'File extension not allowed. Use CSV';
const NON_COMPLIANT_CSV = 'File is not valid';
const OTHER_FAILURE = 'Internal server error';
const SUCCESS = 'File uploaded';

const CsvUploader: FC<CsvUploaderProps> = ({}) => {
    const [documentId,setDocumentId] = documentStore(state => [state.documentId, state.setDocumentId]);
    const [uploadProgress,setUploadProgress] = documentStore(state => [state.uploadProgress, state.setUploadProgress]);
    const [isUploading,setIsUploading] = documentStore(state => [state.isUploading, state.setIsUploading]);
    const [fileToSend,setFileToSend] = documentStore(state => [state.fileToSend, state.setFileToSend]);
    const [status,setStatus] = documentStore(state => [state.status, state.setStatus]);
    const [columnsValid,setColumnsValid] = documentStore(state => [state.columnsValid, state.setColumnsValid]);
    const [notEmpty,setNotEmpty] = documentStore(state => [state.notEmpty, state.setNotEmpty]);

    const handleFileChange = (event: any) => {
        const newFile = event?.target?.files[0];
        if (newFile === null || newFile === undefined) return;
        
        setFileToSend(newFile);
        setUploadProgress(0.0);
        setStatus('');
        setColumnsValid(true);
        setDocumentId(-1);
        setNotEmpty(true);
        
        sendFile(newFile);
    };

   const sendFile = (fileToSend: any) => {
        console.log('WILL SEND', fileToSend);
        if (fileToSend === '') {
            return;
        }
        const serverUrl = `${CONSTANTS.BACKEND_SERVER}/api/upload`;
        const formData = new FormData();
        formData.append("file", fileToSend);

        setIsUploading(false);
        setUploadProgress(0.0);

        const requestConfig = {
            onUploadProgress: (progressEvent: any) => {
                    console.log('GOT', progressEvent);
                    const percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total );
                    setUploadProgress(percentCompleted);
            },
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        };
        
        axios.post(serverUrl, formData, requestConfig)
        .then(res=>{
            console.log('GOT', res);
            const documentId = res?.data?.document_id;
            const status = res?.data?.status;
            const columns_valid = res?.data?.compliance_columns_valid;
            const not_empty = res?.data?.compliance_not_empty;

            console.log('WILL SET', columns_valid, not_empty);
            setIsUploading(false);
            setUploadProgress(100.0);
            setDocumentId(documentId);
            setStatus(status !== undefined ? status : '');
            setColumnsValid(columns_valid !== undefined ? columns_valid : false);
            setNotEmpty(not_empty !== undefined ? not_empty : false);
        })
        .catch(err=>{
            setIsUploading(false);
            console.log(err);
        });
    };

    const boolToStr = (b: boolean) => {
        return b ? "YES" : "NO";
    }
    const isError = false;
    
    return (
        <form id="svs_uploader">
            <h3>CSV upload</h3>
            {}
            <input type="file" onChange={handleFileChange} accept="svs"></input>
            {isError && 
            <div id="upload_error">
                Upload failed    
            </div>}
            {status !== '' && status !== SUCCESS &&
            <div id="error_status">
                <p>File processing failed</p>
                <p>Failure reason: {status}</p>
                {(!columnsValid || !notEmpty) && 
                <div id="aditional_info">
                    <p>Aditional info:</p>
                    <p>Columns valid: {boolToStr(columnsValid)}</p>
                    <p>Not empty: {boolToStr(notEmpty)}</p>
                </div>
                }    
            </div>}
            {documentId !== -1 && !isUploading && !isError &&
            <div id="document_info">
                <p>Upload successfull</p>
                <p>Document id: {documentId}</p>
            </div>}
            {uploadProgress !== 0 && !isUploading && !isError && 
            <div id="progress_tracker">
                <p>Progress: {uploadProgress} %</p>
                <div id="progress_bar" style={{width: uploadProgress + '%'}}></div>
            </div>}
        </form>
    );
}

export default CsvUploader;