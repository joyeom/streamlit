[# 1차 : sm-re-re_sm-re_rv 했는데도 모두 rejected 다시 db로 돌아가서 동일한 sm유저, 다른 rv유저 에게 평가받음
    # re-sm(Question, Answer), re-rv(Answer) 카드에서만 보면 됨 
    question["source"] , answer[tr_list 안에 있는 ["sentence"]들], 



    { #Card_type = SM
        "_id": {},
        "project_id": 250,
        "source_id": 390985,
        "primary_card_id": {},
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "SM",
        "is_reprocessing": "N",
        "status": "F",
        "final_status": "P",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ],
            "source_count": 19,
            "unit_type": "W"
        },
        "points": {
            "base": 304,
            "single_response": 121,
            "waiting_points": 304
        },
        "__v": 0,
        "created_at": "2023-02-24T09:51:52.813Z",
        "updated_at": "2023-03-23T12:57:41.932Z",
        "task_id": {},
        "user_id": 4336947,
        "answer": {
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 86
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 83
                        }
                    ]
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquater: 59 Street No. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 75
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 75
                        }
                    ]
                }
            ],
            "report_reason_id_list": []
        },
        "submitted_at": "2023-03-23T06:21:05.145Z",
        "atomic_tr_log": 1,
        "review_result": "R",
        "user": {
            "user_id": 4336947,
            "username": "ntdat3131999",
            "email": "ntdat3131999@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    },




    {#Card Type = RV
        "_id": {},
        "project_id": 251,
        "source_id": 390985,
        "primary_card_id": {},
        "sm_user_id": 4336947,
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "RV",
        "is_reprocessing": "N",
        "status": "F",
        "final_status": "P",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 86
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 83
                        }
                    ]
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquater: 59 Street No. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 75
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 75
                        }
                    ]
                }
            ],

            "source_count": 19,
            "unit_type": "W",
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ]
        },
        "points": {
            "base": 133,
            "single_response": 66,
            "waiting_points": 133
        },
        "created_at": "2023-03-23T06:35:35.781Z",
        "updated_at": "2023-03-23T13:01:54.169Z",
        "__v": 0,
        "task_id": {},
        "user_id": 4138730,
        "answer": {
            "review_list": [
                {
                    "seq_num": 1,
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        20 #Rejected
                    ],
                    "other_reason": ""
                },
                {
                    "seq_num": 2,
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        20
                    ],
                    "other_reason": ""
                }
            ]
        },
        "review_result": "R",
        "submitted_at": "2023-03-23T12:57:41.904Z",
        "atomic_tr_log": 1,
        "user": {
            "user_id": 4138730,
            "username": "Nguyen111",
            "email": "simulacras70@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    },








    { #card type re-SM
        "_id": {},
        "task_id": {},
        "project_id": 250,
        "source_id": 390985,
        "primary_card_id": {},
        "user_id": 4336947,
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "SM",
        "is_reprocessing": "Y",
        "status": "F",
        "final_status": "N",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 86
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 83
                        }
                    ],
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        20
                    ],
                    "other_reason": ""
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquater: 59 Street No. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 75
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 75
                        }
                    ],
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        20
                    ],
                    "other_reason": ""
                }
            ],
            "unit_type": "W",
            "source_count": 19,
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ]
        },
        "points": {
            "base": 304,
            "single_response": 121,
            "waiting_points": 304,
            "confirmed_points": 0
        },
        "atomic_tr_log": 2,
        "created_at": "2023-03-23T06:35:35.781Z",
        "updated_at": "2023-03-25T02:25:03.977Z",
        "__v": 0,
        "answer": {
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 82
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 78
                        }
                    ]
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquater: 59 St. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 67
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 67
                        }
                    ]
                }
            ],
            "report_reason_id_list": []
        },
        "submitted_at": "2023-03-23T15:39:18.579Z",
        "review_result": "R",
        "user": {
            "user_id": 4336947,
            "username": "ntdat3131999",
            "email": "ntdat3131999@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    },














    {#card_type = Re-RV , is_reprocessing = Yes
        "_id": {},
        "task_id": {},
        "project_id": 251,
        "source_id": 390985,
        "primary_card_id": {},
        "user_id": 4138730,
        "sm_user_id": 4336947,
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "RV",
        "is_reprocessing": "Y",
        "status": "C",
        "final_status": "Y",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 82
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 78
                        }
                    ],
                    "is_accepted": "N"
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquater: 59 St. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 67
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 67
                        }
                    ],
                    "is_accepted": "N"
                }
            ],
            "source_count": 19,
            "unit_type": "W",
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ]
        },
        "points": {
            "base": 133,
            "single_response": 66,
            "waiting_points": 133,
            "confirmed_points": 133
        },
        "created_at": "2023-03-23T15:40:01.918Z",
        "updated_at": "2023-03-25T02:25:03.977Z",
        "__v": 0,
        "answer": {
            "review_list": [
                {
                    "seq_num": 1,
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        20,
                        26
                    ],
                    "other_reason": "don't use \"HCMC\""
                },
                {
                    "seq_num": 2,
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        20,
                        26
                    ],
                    "other_reason": "recommend using \"road 27\" and I don't like the \"HCMC\""
                }
            ]
        },
        "review_result": "R",
        "submitted_at": "2023-03-24T02:23:58.302Z",
        "atomic_tr_log": 1,
        "user": {
            "user_id": 4138730,
            "username": "Nguyen111",
            "email": "simulacras70@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    },





















    {#갑자기 여기서 SM by ntdat3131999
        "_id": {},
        "project_id": 250,
        "source_id": 390985,
        "primary_card_id": {},
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "SM",
        "is_reprocessing": "N",
        "status": "F",
        "final_status": "P",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "unit_type": "W",
            "source_count": 19,
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ]
        },
        "points": {
            "base": 304,
            "single_response": 121,
            "waiting_points": 304
        },
        "submitted_at": "2023-03-25T04:29:41.563Z",
        "created_at": "2023-03-23T06:35:35.781Z",
        "updated_at": "2023-03-25T06:23:36.280Z",
        "__v": 0,
        "task_id": {},
        "user_id": 4336947,
        "answer": {
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street 27, Ward 6, Go Vao District, Ho Chi Minh City, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 93
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 90
                        }
                    ]
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquarter: 59 St. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 66
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 66
                        }
                    ]
                }
            ],
            "report_reason_id_list": []
        },
        "atomic_tr_log": 1,
        "review_result": "R",
        "user": {
            "user_id": 4336947,
            "username": "ntdat3131999",
            "email": "ntdat3131999@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    },



















    { #RV by nguyenthilinhchik62c
        "_id": {},
        "project_id": 251,
        "source_id": 390985,
        "primary_card_id": {},
        "sm_user_id": 4336947,
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "RV",
        "is_reprocessing": "N",
        "status": "F",
        "final_status": "P",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street 27, Ward 6, Go Vao District, Ho Chi Minh City, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 93
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 90
                        }
                    ]
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquarter: 59 St. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 66
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 66
                        }
                    ]
                }
            ],
            "source_count": 19,
            "unit_type": "W",
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ]
        },
        "points": {
            "base": 133,
            "single_response": 66,
            "waiting_points": 133
        },
        "created_at": "2023-03-25T04:32:33.444Z",
        "updated_at": "2023-03-25T06:23:41.583Z",
        "__v": 0,
        "task_id": {},
        "user_id": 4139697,
        "answer": {
            "review_list": [
                {
                    "seq_num": 1,
                    "is_accepted": "Y"
                },
                {
                    "seq_num": 2,
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        26
                    ],
                    "other_reason": "\"HCMC\"?"
                }
            ]
        },
        "review_result": "R",
        "submitted_at": "2023-03-25T06:23:36.248Z",
        "atomic_tr_log": 1,
        "user": {
            "user_id": 4139697,
            "username": "nguyenthilinhchik62c",
            "email": "nguyenthilinhchik62cnsh@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    },














    #Re-SM by ntdat3131999 / is_reprocessing": "Y"
    {
        "_id": {},
        "task_id": {},
        "project_id": 250,
        "source_id": 390985,
        "primary_card_id": {},
        "user_id": 4336947,
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "SM",
        "is_reprocessing": "Y",
        "status": "C",
        "final_status": "Y",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street 27, Ward 6, Go Vao District, Ho Chi Minh City, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 93
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 90
                        }
                    ],
                    "is_accepted": "Y"
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquarter: 59 St. 27, Ward 6, Go Vap District, HCMC, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 66
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 66
                        }
                    ],
                    "is_accepted": "N",
                    "reject_reason_id_list": [
                        26
                    ],
                    "other_reason": "\"HCMC\"?"
                }
            ],
            "unit_type": "W",
            "source_count": 19,
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ]
        },
        "points": {
            "base": 304,
            "single_response": 121,
            "waiting_points": 304,
            "confirmed_points": 304
        },
        "atomic_tr_log": 2,
        "created_at": "2023-03-25T04:32:33.444Z",
        "updated_at": "2023-03-25T20:10:36.336Z",
        "__v": 0,
        "answer": {
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street 27, Ward 6, Go Vao District, Ho Chi Minh City, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 93
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 90
                        }
                    ]
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquarter: 59 St. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 82
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 82
                        }
                    ]
                }
            ],
            "report_reason_id_list": []
        },
        "submitted_at": "2023-03-25T14:35:42.632Z",
        "review_result": "A",
        "user": {
            "user_id": 4336947,
            "username": "ntdat3131999",
            "email": "ntdat3131999@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    },













    {#re-rv by nguyenthilinhchik62c
        "_id": {},
        "task_id": {},
        "project_id": 251,
        "source_id": 390985,
        "primary_card_id": {},
        "user_id": 4139697,
        "sm_user_id": 4336947,
        "src_lang_id": 61,
        "tgt_lang_id": 17,
        "resource_type": "HT",
        "card_type": "RV",
        "is_reprocessing": "Y",
        "status": "C",
        "final_status": "Y",
        "is_golden_set": "N",
        "question": {
            "source": "Trụ sở chính: 59 Đường số 27, Phường 6, Quận Gò Vấp, Thành phố Hồ Chí Minh, Việt Nam.",
            "tr_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street 27, Ward 6, Go Vao District, Ho Chi Minh City, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 93
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 90
                        }
                    ],
                    "is_accepted": "Y"
                },
                {
                    "seq_num": 2,
                    "sentence": "Headquarter: 59 St. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_score": [
                        {
                            "engine": "g",
                            "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 82
                        },
                        {
                            "engine": "m",
                            "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                            "score": 82
                        }
                    ],
                    "is_accepted": "N"
                }
            ],
            "source_count": 19,
            "unit_type": "W",
            "mt_list": [
                {
                    "seq_num": 1,
                    "sentence": "Head office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "g"
                },
                {
                    "seq_num": 2,
                    "sentence": "Head Office: 59 Street No. 27, Ward 6, Go Vap District, Ho Chi Minh City, Vietnam.",
                    "mt_engine": "m"
                }
            ]
        },
        "points": {
            "base": 133,
            "single_response": 66,
            "waiting_points": 133,
            "confirmed_points": 133
        },
        "created_at": "2023-03-25T14:36:15.373Z",
        "updated_at": "2023-03-25T20:10:40.068Z",
        "__v": 0,
        "answer": {
            "review_list": [
                {
                    "seq_num": 1,
                    "is_accepted": "Y"
                },
                {
                    "seq_num": 2,
                    "is_accepted": "Y"
                }
            ]
        },
        "review_result": "A",
        "submitted_at": "2023-03-25T20:10:36.321Z",
        "atomic_tr_log": 1,
        "user": {
            "user_id": 4139697,
            "username": "nguyenthilinhchik62c",
            "email": "nguyenthilinhchik62cnsh@gmail.com",
            "native_lang_id": 61,
            "country_id": 242
        }
    }
]