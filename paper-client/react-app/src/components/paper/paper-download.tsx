
export const downloadPaper = (id: string) => {
    window.open(`http://localhost:5000//api/get-paper-pdf/${id}`, '_blank');
};