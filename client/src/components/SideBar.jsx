import React, { useEffect, useState } from "react";
import { getAllFoldersTree } from "../api/folder.api";
import { FolderTree } from "./FolderTree";
import { CreateFolderModal } from "./CreateFolderModal";

export function SideBar() {
  const [folders, setFolders] = useState([]);
  const [reload, setReload] = useState(false)

  useEffect(() => {
    async function loadFolders() {
      const { data } = await getAllFoldersTree();
      setFolders(data);
    }
    loadFolders();
  }, [reload]);

  const triggerReloadSideBar = () => {
      setReload(!reload)
  }

  return (
    <>
      <FolderTree folders={folders}  triggerReloadSideBar={triggerReloadSideBar} />
    </>
  );
}
