package com.emailSender.emailSenderPMG.dtos;

public record EmailRecordDto(String to,
                             String subject,
                             String text) {
}
