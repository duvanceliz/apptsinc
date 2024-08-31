// import { useEffect, useState } from "react";
// import { getAllFolders } from "../api/folder.api";
// import { FolderCard } from "./FolderCard";


// export function FolderList() {
//   const [folders, setFolders] = useState([]);

//   useEffect(() => {
//     async function loadFolders() {
//       const {data} = await getAllFolders();
//       setFolders(data);
//     }
//     loadFolders();
//   }, []);

//   return <div>
//     { folders.map( folder => (

//         <FolderCard key={folder.id} folder={folder} />
        
        
//     )) }
//   </div>;
// }
