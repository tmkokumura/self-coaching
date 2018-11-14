$(function() {
    /* 質問を変えるボタン押下時 */
    $('#change').click(function(){
        activate();
        change();
    });

    /* 回答するボタン押下時 */
    $('#answer').click(function(){
        activate();
        answer();
    });
})

/* 質問を変えるボタン活性化 */
function activate() {
    $('#change').prop('disabled', false);
}

/* changeメソッドajax呼び出し */
function change() {
    $.ajax({
        url:'change',
        type:'POST',
        data:{
            'prev_answer_hist_id': $('#prev_answer_hist_id').val(),
            'question_id': $('#question_id').val()
        }
    })
    .done(function(res){
        $('#question_id').val(res.question_id);
        $('#question_text').html(res.question_text);
        $('#prev_answer_hist_id').val(res.prev_answer_hist_id);
    })
    .error(function(){
        $('#msg').html('システムエラーが発生しました。');
    })
}

/* answerメソッドajax呼び出し */
function answer() {
    $.ajax({
        url:'answer',
        type:'POST',
        data:{
            'prev_answer_hist_id': $('#prev_answer_hist_id').val(),
            'question_id': $('#question_id').val(),
            'answer_text': $('#answer_text').val()
        }
    })
    .done(function(res){
        $('#question_id').val(res.question_id);
        $('#question_text').html(res.question_text);
        $('#prev_answer_hist_id').val(res.prev_answer_hist_id);
    })
    .error(function(){
        $('#msg').html('システムエラーが発生しました。');
    })
}