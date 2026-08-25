

export default function MovieModal({ title, open, plot, poster, year, onClose }) {
    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
            <div className="rounded-md max-w-lg w-full max-h-[70vh] flex flex-col gap-4 overflow-hidden bg-indigo-300 sm:p-4 p-8 text-white">

                <h2 className="text-[2rem] text-center font-bold"> {title} ({year}) </h2>
                <div className="flex flex-col gap-4 flex-1 overflow-y-auto">

                <span className="break-words shrink-0 lg:text-lg text-md">
                     {plot}
                </span>
                <img className="rounded object-contain max-h-[25vh] h-auto mx-auto" src={poster} alt="" />
                </div>
                <button className="m-2 underline" type="button" onClick={onClose}> close this here panel</button>
            </div>
        </div>
    )
}