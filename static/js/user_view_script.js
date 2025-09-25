// حذف کاربر
$(document).on("click", ".delete-user", function(e){
    e.preventDefault();
    $(this).closest("tr").remove();
});

// اضافه کردن کاربر
$("#addUserBtn").on("click", function(){
    let newRow = 
        <tr>
            <td>
                <img src="https://bootdey.com/img/Content/user_2.jpg" alt="">
                <a href="#" class="user-link">New User</a>
                <span class="user-subhead">Member</span>
            </td>
            <td>${new Date().toISOString().slice(0,10)}</td>
            <td class="text-center">
                <span class="label label-default">pending</span>
            </td>
            <td><a href="#">newuser@mail.com</a></td>
            <td style="width: 20%;">
                <a href="#" class="table-link danger delete-user">
                    <span class="fa-stack">
                        <i class="fa fa-square fa-stack-2x"></i>
                        <i class="fa fa-trash-o fa-stack-1x fa-inverse"></i>
                    </span>
                </a>
            </td>
        </tr>
    ;
    $("#userTable tbody").append(newRow);
});