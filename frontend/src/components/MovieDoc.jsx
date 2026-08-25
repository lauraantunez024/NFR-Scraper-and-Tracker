

export default function MovieModal({ title, plot, tagline, imdb_rating, budget, revenue, poster, year, open, onClose }) {
    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={onClose}>
            <div className="rounded-md max-w-lg w-full max-h-[90vh] flex flex-col gap-2 overflow-hidden bg-indigo-300 sm:p-4 p-8 text-white">

                <h1 className="text-[clamp(1.25rem,4vw,2.2rem)] text-black text-center font-bold"> {title} ({year}) </h1>

                <h2 className="text-center text-[clamp(1rem,4vw,1.4rem)] text-gray-500 italic p-4"> {tagline} </h2>
                <div className="flex flex-col gap-4 flex-1 overflow-y-auto">

                    <span className="break-words shrink-0  text-[clamp(0.9rem,1.6vh,1rem)]">
                        {plot}
                    </span>
                    <img className="rounded object-contain max-h-[25vh] h-auto mx-auto" src={poster} alt="" />
                    <div className="flex flex-row justify-center p-4 gap-4 ">

                        <span> imdb rating: {imdb_rating}</span>
                        <span> budget: {budget}</span>
                        <span> revenue: {revenue}</span>
                    </div>
                </div>
                <button className="m-2 underline border max-w-fit rounded m-auto p-2 text-center border-black-300 bg-white text-black" type="button" onClick={onClose}> close this here panel</button>
            </div>
        </div>
    )
}