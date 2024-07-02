from db.model import get_paper_list_as_list, get_llmprompt_list_as_list, get_paper_metainfo_from_db, insert_llmsummary_record_to_db

if __name__ == "__main__":
    paper_id = "P-00001"
    prompt_id = "L-00001"
    ret = """### Analysis of Evolutionary Multi-Tasking as an Island Model

#### Summary
- **Main Points**: 
    - The paper explores the application of multifactorial evolutionary algorithms (MEFA) to solve multiple optimization tasks simultaneously using genetic programming.
    - The authors propose using an island model for evolutionary multi-tasking, aiming to enhance the results by addressing potential limitations of traditional MEFA.
    - Comparisons between the island model and MEFA are drawn through various computational experiments on different benchmark problems.
    
- **Findings**:
    - The island model demonstrated better performance compared to traditional MEFA, especially on tasks with varied complexity.
    - By limiting interaction between tasks within islands, exploitation capabilities improved, leading to better local optimization.
    - The proposed model effectively addressed problems associated with task interference in evolutionary multi-tasking.

### Analysis
- **Repeated Words**: evolutionary, multi-tasking, MEFA, fitness, tasks, model, optimization, island, algorithm, individual, problem.  

- **General Idea**:  
    - The study aims to enhance evolutionary multi-tasking by employing an island model, where different tasks are isolated into different populations (islands) to improve optimization efficiency and results.

- **Problem**:  
    - The study addresses the problem of interference and negative transfer in multi-task optimization when using traditional MEFA, leading to suboptimal performance.

- **Proposed Solution**:   
    - The island model is proposed as a solution, wherein each island handles a specific task or set of tasks, minimizing negative interference. The migration of individuals between islands is used selectively to balance exploitation and exploration in the search space.
    
    
### Experimental Evaluation
- The experiments used benchmark problems to evaluate the performance of the proposed island model against traditional MEFA. The results indicated that the island model typically outperforms MEFA on various complexity problems, echoing the primary hypothesis behind the model's conceptualization. 
- The findings underscore the significance of managing task interference in evolutionary computation and highlight the potential of island models in addressing this challenge."""

    print(insert_llmsummary_record_to_db(paper_id=paper_id, prompt_id=prompt_id, summary=ret, exist_ok=True))
    # rets = get_llmprompt_list_as_list()
    # for ret in rets:
    #     print(ret)
    # print(get_paper_list_as_list())
