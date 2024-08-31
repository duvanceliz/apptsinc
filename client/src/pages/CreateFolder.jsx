
import { CreateFolderModal } from "../components/CreateFolderModal"
import { useNavigate,useParams } from "react-router-dom"

export function CreateFolder() {
  return (
    <div>
      <CreateFolderModal/>
      <span>Create folder</span>
    </div>
  )
}

