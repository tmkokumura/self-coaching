$(function() {
    /* 質問を変えるボタン押下時 */
    $('#change').click(function(){
        change();
        reset();
    });

    /* 回答するボタン押下時 */
    $('#answer').click(function(){
        answer();
        reset();
    });
})

/* 画面リセット */
function reset() {
    $('#msg').html('');
    $('#change').prop('disabled', false);
    $('#answer_text').val('');
}

/* changeメソッドajax呼び出し */
function change() {
    $.ajax({
        url:'change',
        type:'POST',
        data:{
            'question_hist_id': $('#question_hist_id').val()
        }
    })
    .done(function(res){
        $('#question_hist_id').val(res.question_hist_id);
        $('#question_text').html(res.question_text);
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
            'question_hist_id': $('#question_hist_id').val(),
            'answer_text': $('#answer_text').val()
        }
    })
    .done(function(res){
        $('#question_hist_id').val(res.question_hist_id);
        $('#question_text').html(res.question_text);
    })
    .error(function(){
        $('#msg').html('システムエラーが発生しました。');
    })
}