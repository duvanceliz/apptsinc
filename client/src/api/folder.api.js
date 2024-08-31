import axios from 'axios'


const urlApiFolders = axios.create({
    baseURL: 'http://localhost:8000/api/v1/folder/',
}
)

const urlApiProjects= axios.create({
    baseURL: 'http://localhost:8000/api/v1/projects/',
}
)


export const getAllProjects = ()=>{
    return urlApiProjects.get('/')
}


export const getAllFolders = () =>{
   return urlApiFolders.get('/')
}

export const getAllFoldersTree = () =>{
    return axios.get('http://localhost:8000/api/v1/folders/')
 }

export const getFolder = (id) =>{
    return urlApiFolders.get(`/${id}`)
 }
 
export const createFolder = (folder) => {
    return urlApiFolders.post('/',folder)
}

export const deleteFolder = (id) => {
    return urlApiFolders.delete(`/${id}`)
}
export const updateFolder = (id, folder) => {
    return urlApiFolders.put(`/${id}/`,folder)
}


export const deleteOffer = (id) => {
    return urlApiProjects.delete(`/${id}`)
}

export const createProject = (project) => {
    return urlApiProjects.post('/',project)
}

export const getProject = (id) =>{
    return urlApiProjects.get(`/${id}`)
 }
 