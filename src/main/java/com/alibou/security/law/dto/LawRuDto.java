package com.alibou.security.law.dto;

import com.alibou.security.law.entities.LawType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LawRuDto {
    private UUID id;
    private String name;
    private LawType lawType;
    private String link;
    private String image;
}
