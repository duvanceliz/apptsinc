import { useForm } from "react-hook-form";
import {
  createFolder,
  deleteFolder,
  getAllFoldersTree,
  getFolder,
  updateFolder,
  getAllFolders
} from "../api/folder.api";
import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { toast } from "react-hot-toast";

export function CreateFolderModal({ triggerReloadSideBar, reloadFolderTree }) {
  const navigate = useNavigate();
  const {id} = useParams();


 
  const [folders, setFolders] = useState([]); // Estado para las carpetas
  const [reload, setReload] = useState(false); // Estado de dependencia

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue
  } = useForm();

  const onSubmit = handleSubmit(async (data) => {
    await createFolder(data);
    triggerReloadSideBar()
    triggerReload()
    toast.success("Carpeta creada", {
      position: "bottom-right",
    });

    navigate("/home");
  });

  const triggerReload = () => {
    setReload(!reload); // Cambia el estado para disparar el useEffect
   };


  useEffect(() => {
    async function loadFolders() {
       
      const {data} = await getAllFolders()

      setFolders(data)

      if(id){
        const {data} = await getFolder(id)
        // console.log(data.name)
        setValue("name",data.name)
        
    }
    }
    
    loadFolders(); // Cargar las carpetas cuando se monta el componente
  }, [reload, reloadFolderTree, id]);


  return (
    <div
      className="modal fade"
      id="staticBackdrop"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabIndex="-1"
      aria-labelledby="staticBackdropLabel"
      aria-hidden="true"
    >
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h1 className="modal-title fs-5" id="staticBackdropLabel">
              Crear Carpeta
            </h1>
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div className="modal-body">
            <form onSubmit={onSubmit}>
              <div className="mb-4">
                {errors.name && (
                  <div className="alert alert-danger">
                    Este campo es requerido
                  </div>
                )}
              </div>
              <div className="mb-3">
                <input
                  className="form-control"
                  type="text"
                  placeholder="Nombre"
                  {...register("name", { required: true })}
                />
              </div>

              <div className="mb-3">
              <select
                  className="form-control"
                  {...register("parent", { required: false })}
                >
                  <option value="">Selecciona la carpeta padre (opcional)</option>
                  {folders.map(folder => (
                    <option key={folder.id} value={folder.id}>
                      {folder.name}
                    </option>
                  ))}
                </select>
              </div>
              <button className="btn btn-primary w-100" data-bs-dismiss="modal">
                Guardar
              </button>
            </form>
          </div>
          <div className="modal-footer"></div>
        </div>
      </div>
    </div>
  );
}
