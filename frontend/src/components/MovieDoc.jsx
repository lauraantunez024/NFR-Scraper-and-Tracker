

export default function MovieModal({ title, open, plot, poster, onClose }) {
    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
            <div className="rounded-md max-w-lg max-h-[70vh] flex flex-col gap-4 bg-indigo-300 p-4 text-white">

                <h2 className="text-[2rem] text-center font-bold"> {title} </h2>

                <span>
                     {plot}
                </span>
                <img className="max-h-[80%] w-auto rounded" src={poster} alt="" />
                <button className="m-2 underline" type="button" onClick={onClose}> close this here panel</button>
            </div>
        </div>
    )
}