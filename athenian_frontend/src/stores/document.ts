import create from 'zustand'


export type DocumentState = {
    documentId: number,
    isUploading: boolean,
    uploadProgress: number,
    fileName: string,
    fileToSend: any,
    status: string,
    columnsValid: boolean,
    notEmpty: boolean,
    setDocumentId: (documentId: number) => void,
    setIsUploading: (isUploading: boolean) => void,
    setUploadProgress: (uploadProgress: number) => void,
    setFileName: (fileName: string) => void,
    setFileToSend: (file: any) => void,
    setStatus: (status: string) => void,
    setColumnsValid: (columnsValid: boolean) => void,
    setNotEmpty: (notEmpty: boolean) => void,

}

const documentStore = create<DocumentState>((set) => ({
    documentId: -1,
    uploadProgress: 0.0,
    isUploading: false,
    fileName: '',
    status: '',
    columnsValid: true,
    notEmpty: true,
    fileToSend: null,
    setDocumentId: (documentId: number) => {
        set(state => ({documentId: documentId}))
    },
    setIsUploading: (isUploading: boolean) => {
        set(state => ({isUploading: isUploading}))
    },
    setUploadProgress: (uploadProgress: number) => {
        set(state => ({uploadProgress: uploadProgress}))
    },
    setFileName: (fileName: string) => {
        set(state => ({fileName: fileName}))
    },
    setFileToSend: (file: any) => {
        set(state => ({fileToSend: file}))
    },
    setStatus: (status: string) => {
        set(state => ({status: status}))
    },
    setColumnsValid: (columnsValid: boolean) => {
        set(state => ({columnsValid: columnsValid}))
    },
    setNotEmpty: (notEmpty: boolean) => {
        set(state => ({notEmpty: notEmpty}))
    },
}));

export default documentStore;