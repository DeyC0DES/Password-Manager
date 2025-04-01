package com.password_manager.password_manager.models;

import com.password_manager.password_manager.enums.CodeContextEnum;
import com.password_manager.password_manager.enums.CodeStatsEnum;
import jakarta.persistence.*;

import java.io.Serializable;
import java.util.UUID;

@Entity
public class CodeModel implements Serializable {

    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private UUID id;
    @ManyToOne
    @JoinColumn(name="accountId", referencedColumnName = "id")
    private UserModel userModel;
    private String code;
    private CodeContextEnum context;
    private CodeStatsEnum stats;

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public UserModel getUserModel() {
        return userModel;
    }

    public void setUserModel(UserModel userModel) {
        this.userModel = userModel;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public CodeContextEnum getContext() {
        return context;
    }

    public void setContext(CodeContextEnum context) {
        this.context = context;
    }

    public CodeStatsEnum getStats() {
        return stats;
    }

    public void setStats(CodeStatsEnum stats) {
        this.stats = stats;
    }
}
