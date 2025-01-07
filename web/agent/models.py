from django.db import models

class TaskModel(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    question = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, default='PENDING')
    task_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "user": self.user.id if self.user else None,
            "question": self.question,
            "response": self.response,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }

    def __str__(self):
        return self.response or self.status or self.task_id