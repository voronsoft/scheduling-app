
export const getLessonsForMonth = async (year:number, month:number) => {
    try {
        const response = await fetch(
            `/api_admin/lesson_dates_for_the_month_frontend/${year}-${month}-1`
        );
        const responseToJson = await response.json();
        return responseToJson;
    } catch(e){
        console.error(e);
    }
};